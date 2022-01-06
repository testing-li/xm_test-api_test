#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis


class RedisHelper:
    def __init__(self, host='127.0.0.1', port=6379):
        # decode_responses=True 读取时为字符串
        self.__conn = redis.StrictRedis(host, port, decode_responses=True)

    def public(self, channel, message):
        self.__conn.publish(channel, message)
        return True

    def subscribe(self, channel):
        pub = self.__conn.pubsub()
        pub.subscribe(channel)
        pub.parse_response()
        return pub

    def connect(self):
        return self.__conn


if __name__ == '__main__':
    obj = RedisHelper()
    obj.public('channel1', 'begin')
