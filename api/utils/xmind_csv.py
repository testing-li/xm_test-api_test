# -*- coding: utf-8 -*-
# @File    : xmind_csv.py

from xmindparser import xmind_to_dict
import csv
import re


class XmindToCsv():
    def topics_num(self, value):
        """获取xmind标题个数"""
        try:
            return len(value['topics'])
        except KeyError:
            return 0

    def xmind_title(self, value):
        """获取xmind标题内容"""
        return value.get('title')

    def write_csv(self, filename, case, total):
        """
        写入csv文件，case为列表
        :param filename:
        :param case:
        :return:
        """
        headers = ["模块", "子模块", "功能/页面", "功能点", "用例标题", "前置条件", "测试步骤", "预期结果", "优先级"]

        with open(filename, 'w', encoding='utf-8-sig', newline='')as f:
            f_csv = csv.writer(f)
            f_csv.writerow(headers)
            f_csv.writerows(case)
        print(f"success generate case: {total}")

    def read_xmind(self, filename):
        """
        读取xmind内容，返回case列表
        :param filename:
        :return:
        """
        # xmind内容
        xmind_content = xmind_to_dict(filename)[0]['topic']
        # 主题名
        topic_name = self.xmind_title(xmind_content)
        # 模块/子模块
        if "#" in topic_name:
            module_name = re.compile(r"[\u4e00-\u9fa5]+").findall(topic_name)[0]
            sub_module_name = re.compile(r"[\u4e00-\u9fa5]+").findall(topic_name)[1]
        else:
            module_name = sub_module_name = topic_name  # 模块名
        # 功能的数量
        fun_num = self.topics_num(xmind_content)
        # 用例列表
        case_list = []
        for i in range(fun_num):
            fun_point_num = self.topics_num(xmind_content['topics'][i])
            fun_name = self.xmind_title(xmind_content['topics'][i])
            if fun_point_num == 0:
                print(f'{fun_name}，功能点为空')
                continue
            else:
                for j in range(fun_point_num):
                    fun_point_name = self.xmind_title(xmind_content['topics'][i]['topics'][j])
                    case_point_num = self.topics_num(xmind_content['topics'][i]['topics'][j])
                    if not case_point_num:
                        print(f'{fun_name}，{fun_point_name}，测试用例为空')
                        continue
                    else:
                        for k in range(case_point_num):
                            case = []
                            case_title = self.xmind_title(xmind_content['topics'][i]['topics'][j]['topics'][k])
                            case.append(module_name)
                            case.append(sub_module_name)
                            case.append(fun_name)
                            case.append(fun_point_name)
                            case.append(case_title)
                            # 缺少前置条件处理
                            if not xmind_content['topics'][i]['topics'][j]['topics'][k].get('topics'):
                                case_list.append(case)
                                print(f'{fun_name}，{fun_point_name}，{case_title}，前置条件为空')
                                continue
                            else:
                                case_preconditions = self.xmind_title(
                                    xmind_content['topics'][i]['topics'][j]['topics'][k]['topics'][0])
                                case.append(case_preconditions)
                            # 缺少步骤
                            if not xmind_content['topics'][i]['topics'][j]['topics'][k]['topics'][0].get('topics'):
                                case_list.append(case)
                                print(f'{fun_name}，{fun_point_name}，{case_title}，步骤为空')
                                continue
                            else:
                                case_step = self.xmind_title(
                                    xmind_content['topics'][i]['topics'][j]['topics'][k]['topics'][0]['topics'][0])
                                case.append(case_step)
                            if not xmind_content['topics'][i]['topics'][j]['topics'][k]['topics'][0]['topics'][0].get(
                                    'topics'):
                                case_list.append(case)
                                print(f'{fun_name}，{fun_point_name}，{case_title}，结果为空')
                                continue
                            else:
                                expected_result = self.xmind_title(
                                    xmind_content['topics'][i]['topics'][j]['topics'][k]['topics'][0]['topics'][0][
                                        'topics'][0])
                                case.append(expected_result)
                                case_list.append(case)
        return case_list

    def main(self, xmind_file, csv_file=None):
        """
        :param xmind_file: xmind测试用例的路径
        :param csv_file: 保存为csv格式测试用例的路径，可不填默认保存到对应的xmind测试用例同一路径下
        :return:
        """
        case_list = self.read_xmind(xmind_file)
        if not csv_file:
            csv_file = xmind_file.replace('.xmind', '.csv')
            self.write_csv(csv_file, case_list, len(case_list))
        else:
            self.write_csv(csv_file, case_list, len(case_list))


if __name__ == '__main__':
    xmind_file = r"C:\Users\87859\Desktop\问卷中心#投放.xmind"
    XmindToCsv().main(xmind_file)
