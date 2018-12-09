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


def get_stu_testlist(request):
  ret = {'code': 404, 'info': 'unknown error' }
  ph = PaperHelper()
  # TODO: take out each test and test if the given student is in which tests
  all_paper = Paper.objects.all()
  retlist = []
  for paper in all_paper:
    sl = json.loads(paper.stulist)
    if ph.ExistStu(sl, request.session['login_name']) == True:
      print("[%s] is in paper [%s]." % (request.session['login_name'], paper.pid))
      stucount = json.loads(paper.stulist)['count']
      procount = json.loads(paper.prolist)['problem_count']
      retlist.append(claPaper(paper.pid, paper.pname, paper.teaname,
        paper.penabled, str(stucount), str(procount)))
  jsonarr = json.dumps(retlist, default=lambda o: o.__dict__, sort_keys=True)
  loadarr = json.loads(jsonarr)
  ret = {'code': 200, 'list': loadarr }
  ###
  return HttpResponse(json.dumps(ret), content_type="application/json")


def get_history(request):
  ret = {'code': 200, 'list': 'test history of [%s]' % (request.session['login_name']) }
  return HttpResponse(json.dumps(ret), content_type="application/json")


def get_tea_testlist(request):
  tname = request.session['login_name']
  papers = Paper.objects.filter(teaname = tname)#.all()#
  plist = []
  for var in papers:
    stucount = json.loads(var.stulist)['count']
    procount = json.loads(var.prolist)['problem_count']
    plist.append(claPaper(var.pid, var.pname, var.teaname,
      var.penabled, str(stucount), str(procount)))
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
  ret = {'code': 404, 'info': 'unknown action ' + action }
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

  elif action == 'delete':
    # get the paper id and delete it from database
    Paper.objects.filter(pid = postjson['paperid']).delete()
    ###
    ret = {'code': 200, 'info': 'ok', 'paperid': postjson['paperid'] }

  elif action == 'enable':
    # turn the status of paper to yes
    paperdb = Paper.objects.get(pid = postjson['paperid'])
    paperdb.penabled = 'yes'
    paperdb.save()
    ###
    ret = {'code': 200, 'info': 'ok', 'paperid': postjson['paperid'] }
  elif action == 'disable':
    # turn the status of paper to no
    paperdb = Paper.objects.get(pid = postjson['paperid'])
    paperdb.penabled = 'no'
    paperdb.save()
    ###
    ret = {'code': 200, 'info': 'ok', 'paperid': postjson['paperid'] }

  return HttpResponse(json.dumps(ret), content_type="application/json")


def modify_paper_prolist(request):
  postjson = jh.post2json(request)
  action = postjson['action']
  ret = {'code': 404, 'info': 'unknown action ' + action }
  ph = PaperHelper()

  if action == 'addpro':
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


def modify_paper_stulist(request):
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


def get_test_detail(request):
  ph = PaperHelper()
  ret = {'code': 404, 'info': 'unknown method ' + request.method }
  # GET method means getting test problems
  if request.method == 'GET':
    # TODO: send the test generated back to student
    paperid = request.GET.get('paperid')
    db = Paper.objects.get(pid = paperid)
    paper_pro = json.loads(db.prolist)
    '''
    print(db.prolist)
    test = ph.Paper2test(paper_pro)
    '''
    ###
    
    test = {
      'test_problem': [
        { 'id': '1','problem': '1+1=?','type': 'keguan','point': '5','option1': '5','option2': '2','option3': '4','option4': '3','answer': '',},
        { 'id': '2','problem': '你好吗？','type': 'zhuguan','point': '10','option1': '','option2': '','option3': '','option4': '','answer': '',}
      ] 
    }
    test_info = json.dumps(claPaper(db.pid, db.pname, db.teaname, db.penabled,
      'stulist', 'prolist'), default=lambda o: o.__dict__, sort_keys=True)
    test_info = json.loads(test_info)
    #print(test)
    ret = {'code': 200, 'info': 'ok', 'test': test, 'test_info': test_info }

  # POST method means submitting answers
  elif request.method == 'POST':
    postjson = jh.post2json(request)
    # WAIT: given postjson and get the new json with only answer, id, type, point
    print(postjson['test']['test_problem'])
    ret = {'code': 200, 'info': 'ok', 'stu': request.session['login_name'], 'pname': postjson['pname']}

  return HttpResponse(json.dumps(ret), content_type="application/json")