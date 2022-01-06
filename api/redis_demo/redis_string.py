#!/usr/bin/env python
# -*- coding: utf-8 -*-
from api.redis_demo import redis_helper

con = redis_helper.RedisHelper().connect()
"""
set设置单个key值：
key：键 
value：值
ex：过期时间秒
px: 过期时间毫秒
nx: True 键不存在时复制 None 赋值失败 True 成功
xx: True 键已经存在时才进行赋值 None 赋值失败 True 成功
"""
# con.set("python","test",ex=10,px=1200,nx=True,xx=True)
# print(con.get("python"))
"""
mset(*args, **kwargs)设置多个键值对
get（键）：该函数得到单个键的值，其输入参数是一个字符串。如果该键不存在，返回 None。
mget()：该函数得到一组键的值，其输入和输出都是列表。
strlen(name)： 返回name对应值的字节长度（一个汉字3个字节）
getset()：该函数首先得到指定键原来的值，然后修改其内容，并返回原来的值。如果指定的键不存在，则返回 None。
incr（键，增加量）：如果指定的键不存在，就创建该键，并且值为增加量；如果指定的键已经存在，那么该键值等于原来的值加上增加量。返回值是指定的键操作后的值。注意，增加量只能是整数，不能是浮点数，如果希望用浮点数，则应该使用 incrbyfloat() 函数。
decr（键，减少量）：和 incr() 类似，如果指定的键不存在，创建该键，赋值为减少量的相反数；如果指定的键已经存在，那么该键的值为原来值减去减少量的结果。
append（键，字符串）：该函数用于字符串的连接操作，例如，原来的值是“abc”，现在添加“xyz”，那么结果就是“abcxyz”。如果指定的键原来不存在，则创建该键，返回值是操作后字符串的字节数，
"""
# con.mset({"mset1": "t1", "mset2": "t2"})
# print(con.mget("mset1", "mset2"))
# # con.set("intstring",0)
# con.incr("intstring", 1)
# print(con.get("intstring"))
con.set("visit:12306:totals", 34634)
con.incr("visit:12306:totals",1)
print(con.get("visit:12306:totals"))
print(con.keys())
