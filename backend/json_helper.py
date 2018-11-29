# -*- coding: utf-8 -*-

from django.conf import settings
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from backend.models import UserList, Paper
import json
import os

def post2json(request):
  concat = request.POST
  postBody = request.body
  #print(concat)
  #print(type(postBody))
  #print(postBody)
  json_result = json.loads(postBody)
  #print(json_result)
  return json_result

  