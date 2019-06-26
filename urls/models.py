# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from .util_functions import to_base62, to_base10
from django.contrib.auth.models import User
# Create your models here.

class Url(models.Model):
	full_url = models.CharField(max_length=200)
	short_url = models.CharField(max_length=8,unique=True) 
	time_created = models.DateTimeField(auto_now_add=True)
	time_deactive = models.DateTimeField(null=True)
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,unique=False)
	clicks = models.PositiveIntegerField(default=0)
	is_active = models.BooleanField(default=True)
	
	@classmethod
	def makeshort(cls,full_url,user,end_time=None):
		'''
		temp_short = Url.objects.get(short_url=" ")
		if temp_short:
			temp_short.delete()
			temp_short = None
		'''
		new_url = cls.objects.create(full_url=full_url,short_url=" ",time_deactive=end_time)
		new_url.short_url = to_base62(new_url.id)
		new_url.user = user
		new_url.save() 
		return new_url

	@classmethod
	def getshort(cls,short_url,user=None):
		if user:
			url_object = cls.objects.filter(user=user).get(id=to_base10(short_url))
		else:
			url_object = cls.objects.get(id=to_base10(short_url))
		return url_object
		
	@property
	def clean_list(self):
		return {
		'full_url':self.full_url,'short_url':self.short_url,'time_created':str(self.time_created),
		'time_deactive':str(self.time_deactive),'clicks':self.clicks,'is_active':str(self.is_active)
		}
	
	@classmethod
	def Url_List(cls,user):
		url_list = cls.objects.filter(user = user)
		if url_list and len(url_list): 
			url_list = [url.clean_list for url in url_list]
		else:
			url_list = []
		return url_list
	
	@classmethod
	def DisableOldUrls(cls):
		for url in cls.objects.all().order_by('time_deactive'):
			if url.time_deactive is None:
				pass
			elif url.time_deactive > timezone.now():
				break
			else:
				url.is_active = False
				url.time_deactive = None
				url.save()
class ClickerProfile(models.Model):
	TimeClicked = models.DateTimeField(auto_now_add=True)
	url = models.ForeignKey(Url,on_delete=models.CASCADE,unique=False)
	referer = models.CharField(max_length=255)
	user_agent = models.CharField(max_length=255)
	ip_address = models.CharField(max_length=255)
	
	
	@classmethod
	def makeprofile(cls,request,url):
		clicker = cls.objects.create(url=url,referer = request.META.get('HTTP_REFERER','None')
		,user_agent =request.META.get('HTTP_USER_AGENT','None'),ip_address = request.META.get('REMOTE_ADDR','None')
		)
		clicker.save()
		return clicker
	
	@property
	def information(self):
		return {'time_clicked':str(self.TimeClicked),'referer':self.referer,
		'user_agent':self.user_agent,'ip_address':self.ip_address,
		 'full_url':self.url.full_url,'time_created_url':str(self.url.time_created)
		 }
	@classmethod
	def ClickerList(cls,url):
		clicker_list = cls.objects.filter(url=url).order_by('TimeClicked')
		return [clicker.information for clicker in clicker_list]
		
class ContactData(models.Model):
	full_name = models.CharField(max_length=80)
	email = models.EmailField()
	message = models.TextField(max_length=2000)
	
