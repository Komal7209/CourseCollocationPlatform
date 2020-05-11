# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import course_track,user_info,user
admin.site.register([course_track,user_info,user])
# Register your models here.
