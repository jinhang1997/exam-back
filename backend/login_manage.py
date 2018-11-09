# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.conf import settings
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from backend.models import UserList
from backend import global_vars
import json
import os

def login(request):
  # POST means trying to login
  if request.method == 'POST':
    username = request.POST.get('account')
    password = request.POST.get('password')
    list = UserList.objects.all()
    for var in list:
      if username == var.username and password == var.password:
        request.session['login_name'] = username;
        request.session.modified = True
        # set pages to jump to by users' types
        if var.usertype == 'student':
          request.session['type'] = 'student'
          status = {'code': 200, 'redirect': 'student.html', 'username': username }
        elif var.usertype == 'teacher':
          request.session['type'] = 'teacher'
          status = {'code': 200, 'redirect': 'teacher.html', 'username': username }
        elif var.usertype == 'admin':
          request.session['type'] =  'admin'
          status = {'code': 200, 'redirect': 'admin.html', 'username': username }
        else:
          status = {'code': 403, 'redirect': 'error.html', 'username': username }
          del request.session['login_name']
        return HttpResponse(json.dumps(status), content_type="application/json")
    # login failed
    status = {'code': 403, 'redirect': 'error.html' }
    return HttpResponse(json.dumps(status), content_type="application/json")
  
  # GET means getting login status
  elif request.method == 'GET':
    try:
      uname = request.session["login_name"]
      status = {'code': 200, 'username': uname }     
    except Exception:
      status = {'code': 403, 'info': 'not logged in' }
    return HttpResponse(json.dumps(status), content_type="application/json")

  # other types of request are not allowed
  else:
    return HttpResponse("This request is invalid.")

def myinfo(request):
  ret = {'code': 200, 'info': 'your personal info' }
  return HttpResponse(json.dumps(ret), content_type="application/json")

class User:
  def __init__(self, username, password, usertype):
    self.username = username
    self.password = password
    self.usertype = usertype
  def __repr__(self):
    return repr((self.username, self.password, self.usertype))

def get_all_user(request):
  userlist = UserList.objects.all()
  userarr = []
  for var in userlist:
    userarr.append(User(var.username, var.password, var.usertype))
  print (userarr)
  jsonarr = json.dumps(userarr, default=lambda o: o.__dict__, sort_keys=True)
  print (jsonarr)
  loadarr = json.loads(jsonarr)
  print (loadarr)
  retdata = {'code': 200, 'userlist': loadarr }
  print (retdata)
  return HttpResponse(json.dumps(retdata), content_type="application/json")

def add_user(request):
  database = UserList(username = request.POST.get('username'), password = request.POST.get('password'), usertype = request.POST.get('usertype'))
  database.save()
  status = {'code': 200, 'info': request.POST.get('username') }
  return HttpResponse(json.dumps(status), content_type="application/json")

def delete_user(request):
  user_to_del = request.POST.get('username')
  print (user_to_del)
  database = UserList.objects.get(username = user_to_del)
  database.delete()
  status = {'code': 200, 'info': user_to_del }
  return HttpResponse(json.dumps(status), content_type="application/json")

def logout(request):
  try:
    outname = request.session['login_name']
    del request.session['login_name']
  except Exception:
    status = {'code': 403, 'info': 'not logged in' }
    return HttpResponse(json.dumps(status), content_type="application/json")

  status = {'code': 200, 'info': outname }
  return HttpResponse(json.dumps(status), content_type="application/json")