from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
# Create your models here.
# MVC MODEL VIEW CONTROLLER

class Post(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
    title = models.CharField(max_length=120)
    image = models.FileField(null=True,blank=True)
    content = models.TextField()
    draft=models.BooleanField(default=False)
    publish=models.DateField(auto_now=False,auto_now_add=False)
    read_time=models.TimeField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("detail", kwargs={"id": self.id})
