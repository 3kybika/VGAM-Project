# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from  PIL import Image
from django.db import models

# Create your models here.

class Profile (models.Model):
	User = models.OneToOneField(User,on_delete = models.CASCADE,null = True)
	Avatar = models.ImageField(	upload_to = 'avatars/%Y/%m/%d/%H/',	max_length = 100, default = 'default.jpg')
	AboutMe = models.TextField(max_length = 100, null = True)
	organisation = models.TextField(max_length = 100, null = True)
	Date = models.DateTimeField(auto_now_add = True)

class Comment (models.Model):
	Message = models.TextField(max_length = 100 )
	Expert = models.ForeignKey(Profile, related_name='comentToExpert', on_delete = models.CASCADE)
	Author = models.ForeignKey(Profile, related_name='author', on_delete = models.CASCADE)
	Date = models.DateTimeField(auto_now_add = True)
	NumOfLikes = models.IntegerField(default=0)

class Expert(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    custom_text = models.CharField(max_length=200, default = '')
    points = models.IntegerField(default = 0)
    average_case_size = models.IntegerField(default = 0)
    average_reward = models.IntegerField(default = 0)
    average_return_level = models.IntegerField(default = 0)
    has_complaint = models.BooleanField(default = False)
    has_disqualification = models.BooleanField(default = False)
    has_disciplinary_action = models.BooleanField(default = False)
    
    SRO = models.CharField(max_length=20)
    regions = models.CharField(max_length=300)
    industries = models.CharField(max_length=300)
    rating = models.IntegerField(default = 0)