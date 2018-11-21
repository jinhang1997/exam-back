# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.conf import settings
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from backend.models import UserList
from backend.models import Paper
import json
import os

class claPaper:
  def __init__(self, pid, pname, teaname, penabled, stulist, prolist):
    self.pid = pid
    self.pname = pname
    self.teaname = teaname
    self.penabled = penabled
    self.stulist = stulist
    self.prolist = prolist
  def __repr__(self):
    return repr((self.pid, self.pname, self.teaname,
    self.penabled, self.stulist, self.prolist))

def get_avaliable(request):
  ret = {'code': 200, 'list': 'test list of [%s]' % (request.session['login_name']) }
  return HttpResponse(json.dumps(ret), content_type="application/json")

def get_history(request):
  ret = {'code': 200, 'list': 'test history of [%s]' % (request.session['login_name']) }
  return HttpResponse(json.dumps(ret), content_type="application/json")

def get_tea_testlist(request):
  tname = request.session['login_name']
  print(tname)
  papers = Paper.objects.all()#.filter(teaname = tname)
  print(papers)
  plist = []
  for var in papers:
    plist.append(claPaper(var.pid, var.pname, var.teaname,
      var.penabled, var.stulist, var.prolist))
  print(plist)
  jsonarr = json.dumps(plist, default=lambda o: o.__dict__, sort_keys=True)
  print(jsonarr)
  loadarr = json.loads(jsonarr)
  print(loadarr)
  ret = {'code': 200, 'list': loadarr }
  return HttpResponse(json.dumps(ret), content_type="application/json")
