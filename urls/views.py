# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,Http404,JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Url,ClickerProfile
from .forms import UrlHome,SignUpForm,LoginForm,ContactForm,DisableUrl,DateTimeForm
import json



def index(request):
	if request.method == 'POST':
		form = UrlHome(request.POST)
		TimeDateForm = DateTimeForm(request.POST)
		request_url = None
		if form.is_valid() and TimeDateForm.is_valid():
			request_url = form.cleaned_data['url_entered']
		if request_url:
			user_submit = None
			if request.user.is_authenticated:
				user_submit = request.user
			neo_url  = Url.makeshort(request_url,user_submit,TimeDateForm.GetDatetime())
			shorten_url = request.build_absolute_uri('/')+neo_url.short_url
			return render(request,'urls/display_url.html',{'shorten_url':shorten_url})
		return render(request,'urls/index.html',{'form': form,'timedateform': TimeDateForm })
	else:
		form = UrlHome()
		TimeDateForm = DateTimeForm()
	return render(request,'urls/index.html', {'form':form,'timedateform': TimeDateForm} )




def url_request(request,url):
	try:
		search_url = Url.getshort(url)
		if not search_url.is_active:
			raise Http404("Error: invalid short link")
	except Url.DoesNotExist:
		raise Http404("Error: invalid short link")
	search_url.clicks+=1
	search_url.save()
	ClickerProfile.makeprofile(request,search_url)
	return redirect(search_url.full_url)

def SignUp(request):
	if request.method == "POST":
		form = SignUpForm(data=request.POST)
		if form.is_valid():
			form.save()
			return render(request,'urls/confirmation.html',{'message':"Account Made!"})
		return render(request,'urls/signup.html',{'form':form}) #with error message
	form = SignUpForm()
	return render(request,'urls/signup.html',{'form':form})
	
	
def Login(request):
	if request.method =="POST":
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username = username, password = password)
			if user is not None:
				login(request, user)
				if request.GET.get('next') == "/dashboard/":
					return HttpResponseRedirect('/dashboard/')
				return HttpResponseRedirect('/')
		return render(request,'urls/login.html',{'form':form})
	form = LoginForm()
	return render(request,'urls/login.html',{'form':form})
	
def Contact(request):
	if request.method == "POST":
		form = ContactForm(request.POST)
		if form.is_valid():
			form.save()
			return render(request,'urls/confirmation.html',{'message':"Thank you for contacting us."})
		return render(request,'urls/contact.html',{'form':form}) #with error message
	form = ContactForm()
	return render(request,'urls/contact.html',{'form':form}) 

def Logout(request):
	logout(request)
	return HttpResponseRedirect('/')

@login_required(login_url='/login/')
def Dashboard(request):
	urls = Url.Url_List(request.user)
	if request.GET.get('format') == "json":
		for url in urls:
			url['clickers'] = ClickerProfile.ClickerList( Url.getshort( url['short_url'] ))
		return JsonResponse(dict(urls = urls) )
	return render(request,'urls/dashboard.html',{'urls':urls})
	
@login_required(login_url='/login/')
def InfoShort(request,url):
	try:
		search_url = Url.getshort(url,request.user)
		ErrorForm = True
		if request.method == "POST":
			form = DisableUrl(request.POST)
			formTimeDate = DateTimeForm(request.POST)
			ErrorForm = False
			if form.is_valid():
				ErrorForm = True
				search_url.is_active = not search_url.is_active 
				search_url.save()
			elif formTimeDate.is_valid():
				ErrorForm = True
				search_url.time_deactive = formTimeDate.GetDatetime()
				search_url.save()
		if ErrorForm:
			form = DisableUrl()
			formTimeDate = DateTimeForm()
		clicker_list = ClickerProfile.ClickerList(search_url)
		display_url = search_url.clean_list
		return render(request,'urls/displayurlinfo.html',{
			"url_info":display_url,
			"clickers":clicker_list,
			"form":form,
			"input_val":search_url.is_active,
			"timedateform": formTimeDate
			}
		)
	except Url.DoesNotExist:
		return HttpResponseRedirect('/')
	
@login_required(login_url='/login/')
def InfoClicker(request,url,user_id):
	try:
		search_url = Url.getshort(url,request.user)
		clicker_list = ClickerProfile.ClickerList(search_url)
		display_url = search_url.clean_list
		user_id = int(user_id)
		if user_id > 0 and len(clicker_list) >= user_id:
			clicker_profile = clicker_list[user_id-1]
			return render(request,'urls/clickerinfo.html',{'clicker':clicker_profile})
		return HttpResponseRedirect('/')
	except Url.DoesNotExist:
		return HttpResponseRedirect('/')
		
	
	

