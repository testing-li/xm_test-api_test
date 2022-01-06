#!/usr/bin/env python
# -*- coding: utf-8 -*-
from api.redis_demo import redis_helper

con = redis_helper.RedisHelper().connect()
"""
一、集合
1.新增
sadd(name,values)
2.获取元素个数 类似于len
scard(name)
3.获取集合中所有的成员
smembers(name)
获取集合中所有的成员--迭代器的方式
sscan_iter(name, match=None, count=None)
同字符串的操作，用于增量迭代分批获取元素，避免内存消耗太大
for i in r.sscan_iter("set1"):
    print(i)
4.差集
sdiff(keys, *args)
在第一个name对应的集合中且不在其他name对应的集合的元素集合
5.交集
sinter(keys, *args)
获取多一个name对应集合的交集
6.并集
sunion(keys, *args)
获取多个name对应的集合的并集
7.判断是否是集合的成员 类似in
sismember(name, value)
检查value是否是name对应的集合的成员，结果为True和False
8.删除--随机删除并且返回被删除值
spop(name)
从集合移除一个成员，并将其返回,说明一下，集合是无序的，所有是随机删除的
9.11.删除--指定值删除
srem(name, values)
在name对应的集合中删除某些值
10.集合操作并保存到一个新的集合
{}store(nset,set1,set2..)
二、有序集合
Set操作，Set集合就是不允许重复的列表，本身是无序的
有序集合，在集合的基础上，为每元素排序；元素的排序需要根据另外一个值来进行比较，
所以，对于有序集合，每一个元素有两个值，即：值和分数，分数专门用来做排序。
1.新增
zadd(name, *args, **kwargs)
在name对应的有序集合中添加元素
r.zadd("zset1", n1=11, n2=22)
2.获取有序集合元素个数 类似于len
zcard(name)
3.获取有序集合的所有元素
r.zrange( name, start, end, desc=False, withscores=False, score_cast_func=float)
按照索引范围获取name对应的有序集合的元素
参数：
name，redis的name
start，有序集合索引起始位置（非分数）
end，有序集合索引结束位置（非分数）
desc，排序规则，默认按照分数从小到大排序
withscores，是否获取元素的分数，默认只获取元素的值
score_cast_func，对分数进行数据转换的函数
4. 按照分数范围获取name对应的有序集合的元素
zrangebyscore(name, min, max, start=None, num=None, withscores=False, score_cast_func=float)
5.获取所有元素--默认按照分数顺序排序
zscan(name, cursor=0, match=None, count=None, score_cast_func=float)
6.zcount(name, min, max)
获取name对应的有序集合中分数 在 [min,max] 之间的个数
7.自增
zincrby(name, value, amount)
自增name对应的有序集合的 name 对应的分数
8.删除--指定值删除
zrem(name, values)
删除name对应的有序集合中值是values的成员
9.删除--根据分数范围删除
zremrangebyscore(name, min, max)
10.获取值对应的分数
zscore(name, value)
获取name对应有序集合中 value 对应的分数
"""
print(con.keys())
print(f"set1 元素 {con.smembers('set1')}")
print(f"set2 元素 {con.smembers('set2')}")
# 差
print(f'差集 {con.sdiff("set1","set2")}')
# 并
print(f'交集 {con.sinter("set1","set2")}')
# 交
print(f'并集 {con.sunion("set1","set2")}')
