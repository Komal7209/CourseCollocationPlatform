# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.
class course_track(models.Model):
    mTitle=models.CharField('title',max_length=50)
    mDetail=models.TextField('detail',blank=True)
    mlink=models.CharField('link',max_length=100)
    mimage = models.CharField('title', max_length=50)
    mduration = models.IntegerField('duration')
    mrating=models.FloatField('rating')
    mlevel=models.CharField('level',max_length=20)

class user(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=20)
    mobile=models.IntegerField()
    user_type=models.CharField(max_length=10)
    tracking_id=models.CharField(max_length=40)

class user_info(models.Model):
    email=models.CharField('email',max_length=50)
    password=models.CharField('password',max_length=50)
    name=models.CharField('name',max_length=50)
    profession=models.CharField('profession',max_length=50)