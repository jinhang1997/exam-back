# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.conf import settings
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from backend.models import UserList
import json
import os
 
def login(request):
  # POST means trying to login
  if request.method == 'POST':
    username = request.POST.get('account')
    password = request.POST.get('password')
    # print(username + "is now trying to log in.\n")
    
    list = UserList.objects.all()
    for var in list:
      # print(var.username)
      if username == var.username and password == var.password:
        request.session['login_name'] = username;
        request.session.modified = True
        print('logged: ' + request.session['login_name'])
        status = {'code': 200, 'redirect': 'wait.html', 'username': username }
        return HttpResponse(json.dumps(status), content_type="application/json")
    # login failed
    status = {'code': 403, 'redirect': 'error.html' }
    return HttpResponse(json.dumps(status), content_type="application/json")
  
  # GET means getting login status
  elif request.method == 'GET':
    try:
    #print(request.session.items())
    #print(request.session.get('name', None))
      username = request.session.get(u'login_name', None)
    #print('get login status: ' + usermame)
      status = {'code': 200, 'username': username }     
    except Exception:
      status = {'code': 403, 'info': 'not logged in' }
    return HttpResponse(json.dumps(status), content_type="application/json")

  # other request method are not allowed
  else:
    return HttpResponse("Other methods are invalid")


def logout(request):
  try:
    del request.session['login_name']
  except Exception:
    status = {'code': 403, 'info': 'not logged in' }
    return HttpResponse(json.dumps(status), content_type="application/json")

  status = {'code': 200, 'info': 'log out successfully' }
  return HttpResponse(json.dumps(status), content_type="application/json")


def notfound(request):
  status = {'code': 404, 'info': 'not found' }
  return HttpResponse(json.dumps(status), content_type="application/json")
