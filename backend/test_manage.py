# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.conf import settings
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from backend.models import UserList
import json
import os

def get_all(request):
  ret = {'code': 200, 'list': 'test1' }
  return HttpResponse(json.dumps(ret), content_type="application/json")