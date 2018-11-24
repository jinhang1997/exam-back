import json


class PaperHelper:

    def __init__(self):
        pass

    def __del__(self):
        pass

    def Create(self):
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
        for i in range(0, list_to_del['problem_count']):
            if (questions[i]['id'] == id):
                questions.pop(i)
                break
        list_to_del['problem_count'] -= 1

if __name__ == '__main__':
    pass
