# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.conf import settings
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
import json
import os
 
def login(request):
  # POST means trying to login
  if request.method == 'POST':
    username = request.POST.get('account')
    password = request.POST.get('password')
    print(username)
    if username == 'testuser' and password == 'testpasswd':
      return HttpResponse("{ \"code\": \"200\", \"redirect\": \"wait.html\", \"username\": \"" + str(username) + "\" }") 
    else:
      return HttpResponse("{ \"code\": \"403\", \"redirect\": \"error.html\" }")
  else: # GET means getting login status
    return HttpResponse("Other methods are not implemented yet")

# method to handle requests for normal files
def statics(request):
  realpath = settings.BASE_DIR + '/frontend' + request.path
  #print('real path is :' + realpath)
  with open(realpath, 'rb') as f:
    data_read = f.read()
  return HttpResponse(data_read)

def notfound(request):
  return HttpResponse('404 The path \'' + request.path + '\' is not found.')
