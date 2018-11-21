# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class UserList(models.Model):
  username = models.CharField(max_length = 20, unique = True)
  password = models.CharField(max_length = 20)
  usertype = models.CharField(max_length = 20)

class Paper(models.Model):
  pid = models.CharField(max_length = 20)
  pname = models.CharField(max_length = 20)
  teaname = models.CharField(max_length = 20)
  stulist = models.CharField(max_length = 10240)
  prolist = models.CharField(max_length = 10240)
  penabled = models.CharField(max_length = 20)
