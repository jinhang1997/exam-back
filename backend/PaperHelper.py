import json


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

        # : 'dict'

    def AddPro(self, list_to_append, problem, type, point, right, wrong1, wrong2, wrong3):
        list_to_append['problem_count'] += 1
        obj = {
            'id': list_to_append['id_seed'],
            'problem': problem,
            'type': type,
            'point': point,
            'right': right,
            'wrong1': wrong1,
            'wrong2': wrong2,
            'wrong3': wrong3
        }
        list_to_append['question_list'].append(obj)
        list_to_append['id_seed'] += 1

    #  : 'dict'
    def DelPro(self, list_to_del, id):
        questions = list_to_del['question_list']
        checked = False
        for i in range(0, list_to_del['problem_count']):
            if (questions[i]['id'] == id):
                questions.pop(i)
                checked = True
                break
        if(checked):
            list_to_del['problem_count'] -= 1
        else:
            print('error from PaperHelper DelPro : problem id ' + str(stu_id) + ' does not exist')

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


if __name__ == '__main__':
    pass
