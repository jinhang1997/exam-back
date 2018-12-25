# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.conf import settings
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.db.models import Q
from backend.models import UserList, Paper, TestRecord
import json
import os
import time
from backend.PaperHelper import PaperHelper
from backend import json_helper as jh

class claPaper:
  def __init__(self, pid, pname, teaname, penabled, stulist, prolist, submitted):
    self.pid = pid
    self.pname = pname
    self.teaname = teaname
    self.penabled = penabled
    self.stulist = stulist
    self.prolist = prolist
    self.submitted = submitted

  def __repr__(self):
    return repr((self.pid, self.pname, self.teaname, self.penabled,
      self.stulist, self.prolist, self.submitted))


def get_stu_testlist(request):
  ret = {'code': 404, 'info': 'unknown error' }
  ph = PaperHelper()
  stuid = request.session['login_name']
  # get the list of submitted papers
  test_taken = TestRecord.objects.filter(stuid = stuid)
  takenlist = []
  obj = {}
  for var in test_taken:
    obj['pid'] = var.paperid
    takenlist.append(obj)
    pass
  # take out each test and test if the given student is in which tests
  all_paper = Paper.objects.all()
  retlist = []
  for paper in all_paper:
    sl = json.loads(paper.stulist)
    if ph.ExistStu(sl, stuid) == True:
      #print("[%s] is in paper [%s]." % (stuid, paper.pid))
      stucount = json.loads(paper.stulist)['count']
      procount = json.loads(paper.prolist)['problem_count']
      retlist.append(claPaper(paper.pid, paper.pname, paper.teaname, paper.penabled, 
        str(stucount), str(procount), 'unseen'))
  jsonarr = json.dumps(retlist, default=lambda o: o.__dict__, sort_keys=True)
  loadarr = json.loads(jsonarr)
  ret = {'code': 200, 'list': loadarr, 'taken': takenlist }
  ###
  return HttpResponse(json.dumps(ret), content_type="application/json")


def get_history(request):
  stuid = request.session['login_name']
  records = TestRecord.objects.filter(stuid = stuid)
  obj = {}
  takenlist = []
  for var in records:
    paper = Paper.objects.get(Q(pid = var.paperid))
    obj['pid'] = var.paperid
    obj['pname'] = paper.pname
    obj['teaname'] = paper.teaname
    obj['subtime'] = var.submit_time
    obj['confirmed'] = var.confirmed
    if var.confirmed == 'yes':
      obj['grade'] = var.total_score
    else:
      obj['grade'] = -1
    takenlist.append(obj)
    pass
  ret = {'code': 200, 'list': takenlist }
  return HttpResponse(json.dumps(ret), content_type="application/json")


def get_tea_testlist(request):
  tname = request.session['login_name']
  papers = Paper.objects.filter(teaname = tname)#.all()#
  plist = []
  for var in papers:
    stucount = json.loads(var.stulist)['count']
    procount = json.loads(var.prolist)['problem_count']
    # count the number of whom submitted the answersheet
    subcount = TestRecord.objects.filter(paperid = var.pid).count()
    ###
    plist.append(claPaper(var.pid, var.pname, var.teaname,
      var.penabled, str(stucount), str(procount), str(subcount)))
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
  prolist = json.loads(paper[0].prolist)
  stulist = json.loads(paper[0].stulist)
  subcount = TestRecord.objects.filter(paperid = paperid).count()
  strpaper = json.dumps(claPaper(paper[0].pid, paper[0].pname, paper[0].teaname,
    paper[0].penabled, str(stulist['count']), str(prolist['problem_count']), subcount),
    default=lambda o: o.__dict__, sort_keys=True)
  jsonpaper = json.loads(strpaper)
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

  elif action == 'delall':
    paperid = postjson['paperid']
    paperdb = Paper.objects.get(pid = paperid)
    paperdb.prolist = json.dumps(ph.CreateProList())
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
      if (var == ''):
        continue
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


def test_manage(request):
  ph = PaperHelper()
  ret = {'code': 404, 'info': 'unknown method ' + request.method }
  # GET method means getting test problems
  if request.method == 'GET':
    # TODO: send the test generated back to student
    paperid = request.GET.get('paperid')
    db = Paper.objects.get(pid = paperid)
    paper_pro = json.loads(db.prolist)
    test = ph.Paper2Test(paper_pro)
    ###
    subcount = TestRecord.objects.filter(paperid = paperid).count()
    test_info = json.dumps(claPaper(db.pid, db.pname, db.teaname, db.penabled,
      'notused', 'notused', str(subcount)), default=lambda o: o.__dict__, sort_keys=True)
    test_info = json.loads(test_info)
    #print(test)
    ret = {'code': 200, 'info': 'ok', 'test': test, 'test_info': test_info }

  # POST method means submitting answers
  elif request.method == 'POST':
    postjson = jh.post2json(request)
    #print(postjson)
    # given postjson and get the new json with only answer, id, type, point
    answers = ph.ExtractAnswers(postjson['test'])
    #print(answers)
    answers = json.dumps(answers)
    stuname = request.session['login_name']
    paperid = postjson['paperid']
    if TestRecord.objects.filter(Q(stuid = stuname) & Q(paperid = paperid)).count() > 0:
      ret = {'code': 403, 'info': 'already exists', 'stu': stuname, 'pname': postjson['pname']}
    else:
      db = TestRecord(paperid = paperid, 
        stuid = stuname,
        submit_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        answers = answers,
        keguan_grade = -1,
        keguan_detail = '',
        zhuguan_grade = -1,
        zhuguan_detail = '',
        total_score = -1
        )
      db.save()
      ret = {'code': 200, 'info': 'ok', 'stu': stuname, 'pname': postjson['pname']}

  return HttpResponse(json.dumps(ret), content_type="application/json")


class claRecord:
  def __init__(self, paperid, stuid, submit_time, answers, keguan_grade,
    keguan_detail, zhuguan_grade, zhuguan_detail, total_score, confirmed):
    self.paperid = paperid
    self.stuid = stuid
    self.submit_time = submit_time
    self.answers = answers
    self.keguan_grade = keguan_grade
    self.keguan_detail = keguan_detail
    self.zhuguan_grade = zhuguan_grade
    self.zhuguan_detail = zhuguan_detail
    self.total_score = total_score
    self.confirmed = confirmed

  def __repr__(self):
    return repr((self.paperid, self.stuid, self.submit_time, self.answers, self.keguan_grade,
      self.keguan_detail, self.zhuguan_grade, self.zhuguan_detail, self.total_score))

def judge_manage(request):
  ret = {'code': 200, 'info': 'ok' }
  postjson = jh.post2json(request)
  action = postjson['action']
  paperid = postjson['paperid']
  ph = PaperHelper()
  if action == 'getans':
    ret = {'code': 200, 'info': 'ok' }
    # build the list of all students' answers
    retlist = []
    db = TestRecord.objects.filter(paperid = paperid)
    for var in db:
      retlist.append(claRecord(var.paperid, var.stuid, var.submit_time, var.answers,
        var.keguan_grade, var.keguan_detail, var.zhuguan_grade, var.zhuguan_detail,
        var.total_score, var.confirmed))
    jsonarr = json.dumps(retlist, default=lambda o: o.__dict__, sort_keys=True)
    loadarr = json.loads(jsonarr)
    ret = {'code': 200, 'info': 'ok', 'anslist': loadarr }
    ###

  elif action == 'delans': 
    # delete the specified answer sheet from records
    stuname = postjson['stuname']
    TestRecord.objects.filter(Q(stuid = stuname) & Q(paperid = paperid) & Q(confirmed = 'no')).delete()
    ret = {'code': 200, 'info': 'ok' }
    ###

  elif action == 'submit':
    records = TestRecord.objects.filter(Q(paperid = paperid) & Q(confirmed = 'no'))
    for var in records:
      record = TestRecord.objects.get(Q(stuid = var.stuid) & Q(paperid = paperid) & Q(confirmed = 'no'))
      record.confirmed = 'yes'
      record.total_score = record.keguan_grade + record.zhuguan_grade
      record.save()
      pass
    ret = {'code': 200, 'info': 'ok' }
    pass

  return HttpResponse(json.dumps(ret), content_type="application/json")


def judge_keguan(request): 
  postjson = jh.post2json(request)
  action = postjson['action']
  paperid = postjson['paperid']
  ph = PaperHelper()
  ret = {'code': 404, 'info': 'unknown action ' + action }

  if action == 'judge_keguan':
    # take out each submit and compare with normal answer
    # then save the result into the model.
    paper = Paper.objects.get(pid = paperid)
    answerlist = TestRecord.objects.filter(Q(paperid = paperid) & Q(confirmed = 'no'))
    for var in answerlist:
      #print(var.answers)
      score = ph.JudgeKeguan(json.loads(var.answers), json.loads(paper.prolist))
      #print(score)
      record = TestRecord.objects.get(Q(stuid = var.stuid) & Q(paperid = paperid) & Q(confirmed = 'no'))
      record.keguan_grade = json.dumps(score['score'])
      record.keguan_detail = json.dumps(score['detail'])
      record.save()
      pass
    ret = {'code': 200, 'info': 'ok'}
    ###
    pass

  elif action == 'clean_keguan':
    answerlist = TestRecord.objects.filter(Q(paperid = paperid) 
      & Q(confirmed = 'no')).update(keguan_grade = -1, keguan_detail = "")
    ret = {'code': 200, 'info': 'ok'}
    pass

  return HttpResponse(json.dumps(ret), content_type="application/json")


def judge_zhuguan(request): 
  postjson = jh.post2json(request)
  action = postjson['action']
  paperid = postjson['paperid']
  ph = PaperHelper()
  ret = {'code': 404, 'info': 'unknown action ' + action }

  if action == 'getans':
    stuid = postjson['stuid']
    student = TestRecord.objects.get(Q(stuid = stuid) & Q(paperid = paperid))
    zhuguan = ph.GetZhuguan(json.loads(student.answers))
    judge = {}
    has_judge = 0
    if student.zhuguan_grade != -1:
      judge = student.zhuguan_detail
      judge = json.loads(judge)
      has_judge = 1
    #print(zhuguan)
    ret = { 'code': 200, 'count': zhuguan['count'], 'list': zhuguan['zhuguan_list'],
      'has_judge': has_judge, 'judge': judge, 'confirmed': student.confirmed }
    pass

  elif action == 'submit':
    stuid = postjson['stuid']
    record = TestRecord.objects.get(Q(stuid = stuid) & Q(paperid = paperid) & Q(confirmed = 'no'))
    record.zhuguan_grade = json.dumps(postjson['score'])
    record.zhuguan_detail = json.dumps(postjson['detail'])
    record.save()
    ret = {'code': 200, 'info': 'ok'}
    pass

  elif action == 'clean_zhuguan':
    answerlist = TestRecord.objects.filter(Q(paperid = paperid) 
      & Q(confirmed = 'no')).update(zhuguan_grade = -1, zhuguan_detail = "")
    ret = {'code': 200, 'info': 'ok'}
    pass

  elif action == 'getpro':
    paper = Paper.objects.get(pid = paperid)
    pro = ph.GetProb(json.loads(paper.prolist)['question_list'], postjson['proid'])
    ret = {'code': 200, 'problem': pro['problem'], 'right': pro['right']}
    pass

  elif action == 'nextid':
    records = TestRecord.objects.filter(Q(paperid = paperid) & Q(zhuguan_grade = -1) & Q(confirmed = 'no'))
    if records.count() == 0:
      ret = {'code': 201, 'info': 'no next student is found' }
    else:
      ret = {'code': 200, 'nextid': records[0].stuid }
    pass

  return HttpResponse(json.dumps(ret), content_type="application/json")
