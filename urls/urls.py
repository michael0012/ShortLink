from django.urls import re_path

from . import views

urlpatterns = [
	re_path(r'^$',views.index,name='index'),
	re_path(r'^signup/$',views.SignUp,name='signup'),
	re_path(r'^login/$',views.Login,name='login'),
	re_path(r'^logout/$',views.Logout,name='logout'),
	re_path(r'^contact/$',views.Contact,name='contact'),
	re_path(r'^dashboard/$',views.Dashboard,name='dashboard'),
	re_path(r'^(?P<url>[a-zA-Z0-9]{6})/$',views.url_request),
	re_path(r'^info/(?P<url>[a-zA-Z0-9]{6})/$',views.InfoShort),
	re_path(r'^info/(?P<url>[a-zA-Z0-9]{6})/(?P<user_id>[0-9])/$',views.InfoClicker)
]
