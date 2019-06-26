
from django.urls import include, re_path
from django.contrib import admin

urlpatterns = [
	re_path(r'^',include('urls.urls')),
	re_path(r'^admin/', admin.site.urls),
]
