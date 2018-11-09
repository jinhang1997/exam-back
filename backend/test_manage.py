# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.conf import settings
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from backend.models import UserList
import json
import os

def get_avaliable(request):
  ret = {'code': 200, 'list': 'test list of [%s]' % (request.session['login_name']) }
  return HttpResponse(json.dumps(ret), content_type="application/json")

def get_history(request):
  ret = {'code': 200, 'list': 'test history of [%s]' % (request.session['login_name']) }
  return HttpResponse(json.dumps(ret), content_type="application/json")

def get_tea_testlist(request):
  ret = {'code': 200, 'list': 'test list of [%s]' % (request.session['login_name']) }
  return HttpResponse(json.dumps(ret), content_type="application/json")