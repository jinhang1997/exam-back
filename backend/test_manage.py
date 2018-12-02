# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.conf import settings
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from backend.models import UserList, Paper
import json
import os
import time
from backend.PaperHelper import PaperHelper
from backend import json_helper as jh

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
  papers = Paper.objects.all()#.filter(teaname = tname)
  plist = []
  for var in papers:
    plist.append(claPaper(var.pid, var.pname, var.teaname,
      var.penabled, 'not used', 'not used'))
  jsonarr = json.dumps(plist, default=lambda o: o.__dict__, sort_keys=True)
  loadarr = json.loads(jsonarr)
  ret = {'code': 200, 'list': loadarr }
  return HttpResponse(json.dumps(ret), content_type="application/json")


def get_paper_detail(request):
  paperid = request.GET.get('id')
  # get paper from database
  # TODO(LOW): verify if the specified paper is existing
  ###
  paper = Paper.objects.filter(pid = paperid)
  strpaper = json.dumps(claPaper(paper[0].pid, paper[0].pname, paper[0].teaname,
   paper[0].penabled, 'stulist', 'prolist'),
   default=lambda o: o.__dict__, sort_keys=True)
  jsonpaper = json.loads(strpaper)
  prolist = json.loads(paper[0].prolist)
  stulist = json.loads(paper[0].stulist)
  ret = {'code': 200, 'info': jsonpaper, 'paper': prolist, 'stulist': stulist }
  return HttpResponse(json.dumps(ret), content_type="application/json")


def manage_paper(request):
  postjson = jh.post2json(request)
  action = postjson['action']
  ret = {'code': 404, 'info': 'unknown action' + action }
  ph = PaperHelper()

  if action == 'create':
    # TODO(LOW): verify if the specified paper name is used
    ###
    # get paper name and initialize the new paper with a time id
    database = Paper(pid = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())),
      pname = postjson['papername'],
      teaname = request.session['login_name'],
      penabled = 'no',
      stulist = json.dumps(ph.CreateStuList()),
      prolist = json.dumps(ph.CreateProList()))
    database.save()
    ret = {'code': 200, 'info': 'ok', 'papername': postjson['papername'] }
    return HttpResponse(json.dumps(ret), content_type="application/json")

  elif action == 'delete':
    # TODO: get the paper id and delete it from database
    ###
    ret = {'code': 200, 'info': 'ok' }
    return HttpResponse(json.dumps(ret), content_type="application/json")

  return HttpResponse(json.dumps(ret), content_type="application/json")


def modify_paper(request):
  postjson = jh.post2json(request)
  action = postjson['action']
  ret = {'code': 404, 'info': 'unknown action' + action }
  ph = PaperHelper()

  if action == 'create':
    # TODO: create a new paper and return
    paper = ph.CreateProList()
    print(paper)
    ###
    ret = {'code': 200, 'paper': paper }

  elif action == 'addpro':
    # add problem given in POST packet to paper
    paperid = postjson['paperid']
    problem = postjson['problem']
    # fetch original problem list from database
    paperdb = Paper.objects.get(pid = paperid)
    original_prolist = json.loads(paperdb.prolist)
    ph.AddPro(original_prolist, problem["problem"], problem["ptype"], problem["point"],
     problem["right"], problem["wrong1"], problem["wrong2"], problem["wrong3"])
    paperdb.prolist = json.dumps(original_prolist)
    paperdb.save()
    ret = {'code': 200, 'info': 'ok' }

  elif action == 'delpro':
    # delete problem given in POST packet from paper
    paperid = postjson['paperid']
    problem = postjson['problem']
    paperdb = Paper.objects.get(pid = paperid)
    original_prolist = json.loads(paperdb.prolist)
    ph.DelPro(original_prolist, problem)
    paperdb.prolist = json.dumps(original_prolist)
    paperdb.save()
    ret = {'code': 200, 'paper': 'ok' }

  return HttpResponse(json.dumps(ret), content_type="application/json")


def modify_allow_stulist(request):
  postjson = jh.post2json(request)
  paperid = postjson['paperid']
  action = postjson['action']
  ph = PaperHelper()
  ret = {'code': 404, 'info': 'unknown action' + action }
  # TODO(LOW): verify paperid whether existing
  ###
  paperdb = Paper.objects.get(pid = paperid)

  if (action == 'addstu'):
    stulist = postjson['stulist']
    stuarray = stulist.split('\n')
    original_stulist = json.loads(paperdb.stulist)
    count = 0
    for var in stuarray:
      # TODO(LOW): verify var(stuid) whether existing
      #
      ph.AddStu(original_stulist, var)
      count += 1
    paperdb.stulist = json.dumps(original_stulist)
    paperdb.save()
    ret = {'code': 200, 'info': 'ok', 'count': count }

  elif (action == 'delstu'):
    stu_to_del = postjson['stu_to_del']
    original_stulist = json.loads(paperdb.stulist)
    ph.DelStu(original_stulist, stu_to_del)
    paperdb.stulist = json.dumps(original_stulist)
    paperdb.save()
    ret = {'code': 200, 'info': 'ok', 'deleted': stu_to_del }

  elif (action == 'cleanstu'):
    original_stulist = json.loads(paperdb.stulist)
    count = original_stulist['count']
    empty_list = ph.CreateStuList()
    paperdb.stulist = json.dumps(empty_list)
    paperdb.save()
    ret = {'code': 200, 'info': 'ok', 'count': count }

  return HttpResponse(json.dumps(ret), content_type="application/json")
