from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ContactData
import datetime
import re


class UrlHome(forms.Form):
	url_entered = forms.CharField(
	max_length=150,widget=forms.TextInput(
		attrs={'id':'url_submit','required':True,'placeholder':'Enter URL to Shorten'}
		)
	)
	
	
	def clean_url_entered(self):
		url_submitted = self.cleaned_data['url_entered']
		regex_net = re.compile(
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
		regex_type = re.compile( r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' 
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
		
		if re.match(regex_net,url_submitted) is None and re.match(regex_type,url_submitted) is None:
			raise ValidationError(_("Invalid Url"),code="URL Invalid" )
		elif re.match(regex_type,url_submitted) is None:
			url_submitted = "http://"+url_submitted
			return url_submitted
		else:
			return url_submitted
			
		
		
class DateTimeForm(forms.Form):
	
	date_entered = forms.DateField(
	required=False,widget=forms.DateInput(attrs={'type':'date','required':False})
	)
	
	time_entered = forms.TimeField(
		required=False,widget=forms.TimeInput(attrs={'type':'time','required':False})
	)
	time_zone_entered = forms.IntegerField(
		required = False,
		max_value=840,min_value=-720,
			widget=forms.HiddenInput(
				attrs = {'required':False,"value":0,"id":"time_zone"}
			)
		)
	finalDateTime = None
	
	def clean(self):
		false_datetime = False
		cleaned_data = super(DateTimeForm,self).clean()
		cleaned_date, cleaned_time = self.cleaned_data.get('date_entered',None),self.cleaned_data.get('time_entered',None)
		cleaned_timezone = self.cleaned_data.get('time_zone_entered', None)
		if cleaned_time is None and cleaned_date:
			self.add_error('time_entered',_("Time Field Empty and Data Entered"))
			false_datetime = True
		if cleaned_date is None and cleaned_time:
			self.add_error('date_entered',_("Date Field Empty and Time Entered"))
			false_datetime =True
		if not false_datetime and cleaned_date and cleaned_time and not ( cleaned_timezone == None):
			datetime_entered = timezone.make_aware( 
			datetime.datetime.combine(cleaned_date, cleaned_time) +
				datetime.timedelta(minutes=cleaned_timezone) 
			)
			if datetime_entered < timezone.make_aware(datetime.datetime.now()):
				self.add_error('date_entered',_("Datetime is expired"))
			else:
				self.finalDateTime = datetime_entered
	
	def GetDatetime(self):
		return self.finalDateTime
	
	

class SignUpForm(UserCreationForm):
	email = forms.EmailField(required=True,label="Email", widget=
		forms.EmailInput(attrs={'required':True,'class':'input-holder-type'}  )
	)
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
		
		
	def __init__(self,*args,**kwargs):
		super(SignUpForm,self).__init__(*args,**kwargs)
		self.fields['username'].widget.attrs['class'] = 'input-holder-type'
		self.fields['password1'].widget.attrs['class'] = 'input-holder-type'
		self.fields['password2'].widget.attrs['class'] = 'input-holder-type'
		
	def clean_username(self):
		username = self.cleaned_data['username']
		if username and User.objects.filter(username = username).count():
			raise ValidationError(_("Username exist!"),code="Username Exist")
		return username
	
	def clean_email(self):
		email = self.cleaned_data['email']
		if email and User.objects.filter(email = email).count():
			raise ValidationError(_("Email exist in system!"),code="Email Exist")
		return email
	
	def save(self,commit=True):
		user = super(SignUpForm,self).save(commit=False)
		self.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class LoginForm(forms.Form):
	username = forms.CharField(required=True,label="Username",widget=
		forms.TextInput(attrs={'required':True,'class':'input-holder-type'}  )
	)
	password = forms.CharField(required=True,label="Password",widget=
		forms.PasswordInput(attrs={'required':True,'class':'input-holder-type'}  )
	)
	
class ContactForm(forms.ModelForm):
	class Meta:
		model = ContactData
		fields = '__all__'
		widgets = {
		    'full_name': forms.TextInput(attrs={'required':True,'class':'input-holder-type'} ),
			'email': forms.EmailInput(attrs={'required':True,'class':'input-holder-type'}  ),
		    'message': forms.Textarea(attrs={'required':False})
		}
	def clean_full_name(self):
		#this is a test...
		full_name = self.cleaned_data['full_name']
		if len(full_name) < 1:
			raise ValidationError(_("Your name's length is less than one"),code="Full Name Invalid" )
		else:
			return full_name

class DisableUrl(forms.Form):
	input_check = forms.CharField(required=True,
		widget=forms.HiddenInput(attrs = {'required':True,"value":"CHECK"})
	)


	
