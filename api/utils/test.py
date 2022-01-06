#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
import urllib3
import random
import collections


def random_pick(some_list, probabilities):
    x = random.uniform(0, 1)
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x <= cumulative_probability:
            break
    return item


def random_pick_more(some_list, probabilities):
    x = random.uniform(0, 1)
    l = []
    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability:
            l.append(item)
    return l


def test_random(nu):
    a = [1, 2, 3, 4]
    b = [0.1, 0.2, 0.3, 0.4]
    re = dict(zip(a, [0] * 4))
    for x in range(nu):
        result = random_pick(a, b)
        re[result] += 1
    for v, value in re.items():
        re[v] = float(value) / nu
    return re


def proportional_distribution(list1, list2):
    list_new = []
    total_probability = 0
    for i in list2:
        total_probability += i
    num = [round(i * 100 / total_probability) for i in list2]
    # print(num)
    for i in range(len(list1)):
        for j in range(int(num[i])):
            list_new.append(list1[i])
    choose_list = []
    for i in range(len(list1)):
        option = random.choice(list_new)
        choose_list.append(option)
    choose_option = list(set(choose_list))
    print(choose_option)
    return choose_option


def test1(list1, num):
    d = []
    res = {}
    for i in range(num):
        option = random.choice(list1)
        d.append(option)
    for i in list(set(list1)):
        res[str(i)] = d.count(i)
    print(res)


def test2():
    list1 = [1, 2, 3, 4, 5]
    list2 = [0.12, 0.35, 0.6, 0.1, 0.2]
    d = {}
    option_choose = []
    for i in range(len(list1)):
        d[str(list1[i])] = []
        for j in range(100):
            if j < list2[i] * 100:
                d[str(list1[i])].append(list1[i])
            else:
                d[str(list1[i])].append(0)
    for k, v in d.items():
        option_choose.append(random.choice(v))
    option_mutil = [i for i in option_choose if i != 0]
    if not option_mutil:
        for k, v in d.items():
            option_choose.append(random.choice(v))
    option_mutil = [i for i in option_choose if i != 0]
    return option_mutil


def test_probability(num):
    list1 = [1, 2, 3, 4, 5]
    total = []
    res = {}
    for i in range(num):
        result = test2()
        for j in result:
            total.append(j)
    for i in list1:
        res[str(i)] = total.count(i) / num
    print(res)


if __name__ == '__main__':
    test_probability(1000)
    # list1 = [1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 4]
    # test1(list1, 1000)
    # list1 = ["a", "b", "c"]
    # list2 = [0.4, 0.5, 0.6]
    # # proportional_distribution(list1,list2)
    # test_probability(100)
    # l = [1,1,1,1,2,2,2,3,3,4,5,5,5,5,5]
    # print(random.sample(l, 5))
    # # print(random.uniform(0, 1))
    # a = [1, 2, 3, 4]
    # b = [0.1, 0.2, 0.3, 0.4]
    # for i in range(10):
    #     print(random_pick(a, b))
    # print(test_random(200))
