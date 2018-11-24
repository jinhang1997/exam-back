# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from backend import models

# Register your models here.
class UserListAdmin(admin.ModelAdmin):
    list_display = ['username', 'password', 'usertype']

class PaperAdmin(admin.ModelAdmin):
    list_display = ['pid', 'pname', 'teaname', 'penabled', 'stulist', 'prolist']

admin.site.register(models.UserList, UserListAdmin)
admin.site.register(models.Paper, PaperAdmin)
