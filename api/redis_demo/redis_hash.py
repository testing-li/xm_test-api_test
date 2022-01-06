#!/usr/bin/env python
# -*- coding: utf-8 -*-
from api.redis_demo import redis_helper

con = redis_helper.RedisHelper().connect()
"""
哈希就是键值对组成的集合
1.单个/批量(mapping参数)增加--修改(单个取出)--没有就新增，有的话就修改
hset(name, key, value)
name对应的hash中设置一个键值对（不存在，则创建；否则，修改）
hsetnx(name, key, value),当name对应的hash中不存在当前key时则创建（相当于添加）
2 批量增加
hset(name, mapping=dict)
在name对应的hash中批量设置键值对
参数：
name，redis的name
mapping，字典，如：{'k1':'v1', 'k2': 'v2'}
3 单个取出 返回一个字符串
hget(name,key)
在name对应的hash中获取根据key获取value
4 批量取出 返回一个列表
hmget(name, keys, *args)
在name对应的hash中获取多个key的值
参数：
name，reids对应的name
keys，要获取key集合，如：['k1', 'k2', 'k3']
*args，要获取的key，如：k1,k2,k3
5.取出所有的键值对 返回一个字典
hgetall(name)
6 获取name对应的hash中键值对的个数 返回int
hlen(name)
7 得到所有的keys（类似字典的取所有keys）返回列表
hkeys(name)
8 得到所有的value（类似字典的取所有value）返回列表
hvals(name)
9 判断成员是否存在（类似字典的in）返回boolen
hexists(name, key)
10 删除键值对
hdel(name,*keys)
将name对应的hash中指定key的键值对删除
11 hscan_iter(name, match=None, count=None) 分片优化内存
利用yield封装hscan创建生成器，实现分批去redis中获取数据
参数：
match，匹配指定key，默认None 表示所有的key
count，每次分片最少获取个数，默认None表示采用Redis的默认分片个数
"""
# con.lpush("plist", 1, 2, 3, 4)
# con.hset("phash", "key1", "value1")
# print(con.keys())
# print((con.hgetall("hash1")))
if __name__ == '__main__':
    print(con.keys())
    print(con.hgetall("hash1"))
    con.hset("hash1","key34","test34",mapping={"key30":"test30","key31":"test31"})
    print(con.hgetall("hash1"))

