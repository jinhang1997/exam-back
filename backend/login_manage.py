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
    ulist = UserList.objects.all()
    for var in ulist:
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
  #print (userarr)
  jsonarr = json.dumps(userarr, default=lambda o: o.__dict__, sort_keys=True)
  #print (jsonarr)
  loadarr = json.loads(jsonarr)
  #print (loadarr)
  retdata = {'code': 200, 'userlist': loadarr }
  #print (retdata)
  return HttpResponse(json.dumps(retdata), content_type="application/json")

def if_user_exist(uname):
  #print(uname)
  if UserList.objects.filter(username = uname).count() > 0:
    return True
  else:
    return False

def add_user(request):
  uname = request.POST.get('username')
  print(uname + ' to be add')
  if if_user_exist(uname) == True:
    status = {'code': 403, 'info': uname + ' is already existing' }
    return HttpResponse(json.dumps(status), content_type="application/json")
  database = UserList(username = uname, password = request.POST.get('password'), usertype = request.POST.get('usertype'))
  database.save()
  status = {'code': 200, 'info': uname }
  return HttpResponse(json.dumps(status), content_type="application/json")

def add_user_batch(request):
  #print(request.POST.get('batch_names'))
  addlist = request.POST.get('batch_names').split('\n')
  success_count = 0
  for var in addlist:
    single = var.split()
    print(single[0] + '#' + single[1] + '#' + single[2])
    if if_user_exist(single[0]) == True:
      status = {'code': 403, 'info': single[0] + ' exists already, but ' + str(success_count) + ' succeed' }
      return HttpResponse(json.dumps(status), content_type="application/json")
    if single[2] != 'student' and single[2] != 'teacher':
      status = {'code': 403, 'info': single[0] + ' has an invalid type ' + single[2] + ' ,but ' + str(success_count) + ' succeed' }
      return HttpResponse(json.dumps(status), content_type="application/json")
    db = UserList(username = single[0], password = single[1], usertype = single[2])
    db.save()
    success_count = success_count + 1
  status = {'code': 200, 'info': success_count }
  return HttpResponse(json.dumps(status), content_type="application/json")

def delete_user(request):
  user_to_del = request.POST.get('username')
  print (user_to_del)
  #database = UserList.objects.get(username = user_to_del)
  #database.delete()
  UserList.objects.filter(username = user_to_del).delete()
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