#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
# import random
# import numpy as np
#
# l1 = ["a", "b", "c", "d"]
# p = [0.5, 0.6, 0.3, 0.1]
# # s = np.random.choice(l1, size=3, p=p)
# d = []
# pp = {}
#
#
# def sc(l1, p):
#     p = [i - 0.03 for i in p]
#     choose_data = []
#     for k, v in zip(l1, p):
#         pp[k] = list(k) * int((v * 100)) + [None] * int((1 - v) * 100)
#         choose = np.random.choice(pp[k])
#         choose_data.append(choose)
#     p_data = [i for i in choose_data if i is not None]
#     if p_data == []:
#         p_data = [random.choice(l1)]
#     return p_data
#
#
# def test1(l, p, num):
#     for i in range(num):
#         choose = sc(l, p)
#         d.extend(choose)
#     res = {}
#     for i in l1:
#         res[i] = d.count(i) / num
#     print(res)
#
#
# if __name__ == '__main__':
#     l1 = ["a", "b", "c", "d"]
#     p = [0.3, 0.6, 0.3, 0.1]
#     test1(l1, p, 1000)
import random

a = {"1": {"a": 5, "b": 3, "c": 7}}
num = 10
answer = {}
long = 0
l = []


def multiple_choose():
    long = 0
    for k, v in a["1"].items():
        long += v
        if long < num and long > 0:
            for i in range(v):
                l.append([[k]])
        if long >= num:
            last = num + v - long
            random.shuffle(l)
            for i in range(last):
                l.append([[k]])
            for i in range(long - num):
                l[i].append([k])
            long = -9999
            continue
        if long < 0:
            for i in range(v):
                l[i].append([k])
