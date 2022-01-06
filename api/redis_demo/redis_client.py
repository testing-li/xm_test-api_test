#!/usr/bin/env python
# -*- coding: utf-8 -*-
from api.redis_demo import redis_helper

obj = redis_helper.RedisHelper()
redis_sub = obj.subscribe('channel1')

while True:
    msg = redis_sub.parse_response()
    print(msg)
