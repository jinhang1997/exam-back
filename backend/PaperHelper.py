# -*- coding: utf-8 -*-

import json
import random


class PaperHelper:

    def __init__(self):
        pass

    def __del__(self):
        pass

    def CreateProList(self):
        obj = {
            'problem_count': 0,
            'id_seed': 1,
            'question_list': []
        }
        return obj

    def AddPro(self, list_to_append, problem, ptype, point, right, wrong1, wrong2, wrong3):
        list_to_append['problem_count'] += 1
        obj = {
            'id': list_to_append['id_seed'],
            'problem': problem,
            'type': ptype,
            'point': point,
            'right': right,
            'wrong1': wrong1,
            'wrong2': wrong2,
            'wrong3': wrong3
        }
        list_to_append['question_list'].append(obj)
        list_to_append['id_seed'] += 1

    def DelPro(self, list_to_del, id):
        questions = list_to_del['question_list']
        checked = False
        for i in range(0, list_to_del['problem_count']):
            if (questions[i]['id'] == id):
                questions.pop(i)
                checked = True
                break
        if (checked):
            list_to_del['problem_count'] -= 1
        else:
            print('error from PaperHelper DelPro : problem id ' + str(id) + ' does not exist')

    def CreateStuList(self):
        obj = {
            'count': 0,
            'stu_list': []
        }
        return obj

    def AddStu(self, stu_list, stu_id):
        stu_obj = {'stu': stu_id}
        stu_list['stu_list'].append(stu_obj)
        stu_list['count'] += 1

    def DelStu(self, stu_list, stu_id):
        students = stu_list['stu_list']
        stu_obj = {'stu': stu_id}
        try:
            i = students.index(stu_obj)
            students.pop(i)
            stu_list['count'] -= 1
        except:
            print('error from PaperHelper DelStu : student id ' + str(stu_id) + ' does not exist')

    def ExistStu(self, stu_list, stu_id):
        students = stu_list['stu_list']
        stu_obj = {'stu': stu_id}
        if (stu_obj in students):
            return True
        else:
            return False

    def Paper2Test(self, prolist):
        questions = prolist['question_list']
        test_questions = []
        for question in questions:
            test_question = {}
            if (question['type'] == 'keguan'):
                options = []
                options.append(question['right'])
                for i in range(1, 4):
                    options.append(question['wrong' + str(i)])
                random.shuffle(options)
                test_question = {
                    'id': question['id'],
                    'problem': question['problem'],
                    'type': question['type'],
                    'point': question['point'],
                    'option1': options[0],
                    'option2': options[1],
                    'option3': options[2],
                    'option4': options[3],
                    'answer': '',
                }
            elif (question['type'] == 'zhuguan'):
                test_question = {
                    'id': question['id'],
                    'problem': question['problem'],
                    'type': question['type'],
                    'point': question['point'],
                    'option1': '',
                    'option2': '',
                    'option3': '',
                    'option4': '',
                    'answer': '',
                }
            test_questions.append(test_question)
        return {'test_problem': test_questions}

    def ExtractAnswers(self, test_problem):
        answer_list = []
        problems = test_problem['test_problem']
        for problem in problems:
            answer = {
                'id': problem['id'],
                'point': problem['point'],
                'type': problem['type'],
                'answer': problem['answer']
            }
            answer_list.append(answer)
        return {'answer_list': answer_list}

    def GetProb(self, problems, id):
        the_problem = {}
        for problem in problems:
            if (problem['id'] == id):
                the_problem = problem.copy()
                break
        return the_problem

    def JudgeKeguan(self, answer_list, problem_list):
        answers = answer_list['answer_list']
        problems = problem_list['question_list']
        results = []
        score = 0
        for answer in answers:
            if (answer['type'] == 'keguan'):
                # 两个list经过前端和网络以后顺序可能不一样，所以要根据id再匹配一遍
                problem = self.GetProb(problems, answer['id'])
                if (answer['answer'] == problem['right']):
                    score += problem['point']
                    result = {
                        'id': problem['id'],
                        'grade': problem['point']
                    }
                else:
                    result = {
                        'id': problem['id'],
                        'grade': 0
                    }
                results.append(result)
        result_sum = {
            'keguan_score': score,
            'keguan_detail': results
        }
        return result_sum

    def GetZhuguan(self, answer_list):
        answers = answer_list['answer_list']
        zhuguan_list = []
        for answer in answers:
            if (answer['type'] == 'zhuguan'):
                zhuguan_list.append(answer)
        return {"zhuguan_list":zhuguan_list}

    if __name__ == '__main__':
        pass
