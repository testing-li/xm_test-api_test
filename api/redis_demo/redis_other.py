#!/usr/bin/env python
# -*- coding: utf-8 -*-
from api.redis_demo import redis_helper

con = redis_helper.RedisHelper().connect()
"""
1.删除key
delete(*names)
根据删除redis中的任意数据类型（string、hash、list、set、有序set）
2.检查key是否存在
exists(name)
检测redis的name是否存在，存在就是True，False 不存在
3.查看key
keys(pattern='')
根据模型获取redis的key,默认*
4.设置超时时间
expire(name ,time)
为某个redis的某个name设置超时时间
5.重命名
rename(src, dst)
对redis的name重命名
6.获取类型
type(name)
获取name对应值的类型
7.查看key对应的value
print(r.hscan("hash2"))
print(r.sscan("set3"))
print(r.zscan("zset2"))
print(r.getrange("foo1", 0, -1))
print(r.lrange("list2", 0, -1))
print(r.smembers("set3"))
print(r.zrange("zset3", 0, -1))
print(r.hgetall("hash1"))
8.dbsize()  
当前redis包含多少条数据
9.save()
执行"检查点"操作，将数据写回磁盘。保存时阻塞
10.flushdb()
清空r中的所有数据
11.管道（pipeline）
redis默认在执行每次请求都会创建（连接池申请连接）和断开（归还连接池）一次连接操作，
如果想要在一次请求中指定多个命令，则可以使用pipline实现一次请求指定多个命令，并且默认情况下一次pipline 是原子性操作。
pipe.set('hello', 'redis').sadd('faz', 'baz').incr('num').execute()
"""
