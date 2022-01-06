# -*- coding: utf-8 -*-
from api.utils.gen_qdes import answer_questionnaire
from api.utils import excel_data

ques_data = {}


def change_gid(answer_list, gid_begin):
    a = []
    for i in range(len(answer_list)):
        if answer_list[i] == "选择":
            a.append([gid_begin + i])
    return a


def title_to_gid(data, title, s):
    gid = []
    for i in data[s]['items']:
        if i['title'] == title:
            gid.append(i['gid'])
    return gid


def answer_data(data, base):
    ip = data[15]
    time = data[7:9]
    Q1_answer = data[30]
    Q2_answer = data[31:37]
    Q3_answer = data[37]
    Q4_answer = change_gid(data[38:53], 15)
    Q5_answer = change_gid(data[54:69], 31)
    Q6_answer = change_gid(data[70:86], 47)
    Q7_answer = data[86]
    Q8_answer = title_to_gid(base, data[87], 7)
    Q9_answer = title_to_gid(base, data[88], 8)
    Q10_answer = title_to_gid(base, data[89], 9)
    Q11_answer = title_to_gid(base, data[90], 10)
    if data[91]:
        Q12_answer = [data[91]]
    else:
        Q12_answer = []
    answer = {'3': {'4': [Q1_answer, '', '']},
              '5': {'6': [Q2_answer[0], '', ''], '7': [Q2_answer[1], '', ''], '8': [Q2_answer[2], '', ''],
                    '9': [Q2_answer[3], '', ''],
                    '10': [Q2_answer[4], '', ''], '11': [Q2_answer[5], '', '']}, '12': {'13': [Q3_answer, '', '']},
              '14': Q4_answer,
              '30': Q5_answer,
              '46': Q6_answer, '62': {'63': [Q7_answer, '', '']}, '64': Q8_answer, '68': Q9_answer, '73': Q10_answer,
              '76': Q11_answer,
              '84': Q12_answer}
    return answer, ip, time


if __name__ == '__main__':
    url = 'https://bestcem.com/t/55rbsE'
    base = answer_questionnaire.baseinfo(url)['data']
    a = excel_data.Excel()
    data = a.read_excel(r'../data/file/txtanls.xlsx')
    # for i in data:
    #     print(i)
    # for i in range(200):
    #     s = answer_data(data[i + 3], base)
    #     answer_questionnaire.answer_by_fix_data(s[0], s[1], s[2][0].strftime("%Y/%m/%d %H:%M:%S"),
    #                                             s[2][1].strftime("%Y/%m/%d %H:%M:%S"))
    for i in range(10):
        answer = {"2": [data[i + 1][0]], "4": [data[i + 1][1]], "5": [data[i + 1][2]]}
        begin = data[i + 1][3].strftime("%Y/%m/%d %H:%M:%S")
        end = data[i + 1][4].strftime("%Y/%m/%d %H:%M:%S")
        answer_questionnaire.answer_by_fix_data(answer, "", begin, end)
