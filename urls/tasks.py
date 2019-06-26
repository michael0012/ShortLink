from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import Url


@shared_task
def expired_urls():
	Url.DisableOldUrls()
	print "Disabling Urls"
