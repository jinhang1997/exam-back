# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from backend import models

# Register your models here.
class UserListAdmin(admin.ModelAdmin):
    list_display = ['username','password', 'usertype']

admin.site.register(models.UserList, UserListAdmin)
