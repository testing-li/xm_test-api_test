#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis

# redis-py使用connection pool来管理对一个redis server的所有连接，避免每次建立、释放连接的开销。默认，每个Redis实例都会维护一个自己的连接池。
# 可以直接建立一个连接池，然后作为参数Redis，这样就可以实现多个Redis实例共享一个连接池
conn_pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
# 第一个客户端访问
r1 = redis.StrictRedis(connection_pool=conn_pool)
# 第二个客户端访问
r2 = redis.StrictRedis(connection_pool=conn_pool)
try:
    for i in range(5):
        r1.lpush("queue", f'value{i}')
except Exception as e:
    print(e)
# 读取队列
while True:
    if r2.llen("queue"):
        print(f'{r2.client_id()} 读取 {r2.rpop("queue")}')
