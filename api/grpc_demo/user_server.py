#!/usr/bin/env python
# -*-coding: utf-8 -*-

from concurrent import futures
import grpc
import logging
import time

from api.grpc_demo.rpc_package.userinfo_pb2_grpc import add_UserInfoServiceServicer_to_server, \
    UserInfoServiceServicer
from api.grpc_demo.rpc_package.userinfo_pb2 import UserInfoRequest, UserInfoReply


class UserInfo(UserInfoServiceServicer):

    # 这里实现我们定义的接口
    def GetUserInfo(self, request, context):
        if not request.name:
            return UserInfoReply(code=401,message="name is required")
        else:
            name = request.name
            age = 18
            gender = 1
            date = '2021-06-01'
        return UserInfoReply(name=name, age=age, gender=gender, date=date)


def serve():
    # 这里通过thread pool来并发处理server的任务
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 将对应的任务处理函数添加到rpc server中
    add_UserInfoServiceServicer_to_server(UserInfo(), server)

    # 这里使用的非安全接口，世界gRPC支持TLS/SSL安全连接，以及各种鉴权机制
    server.add_insecure_port('[::]:8881')
    server.start()
    print("server start")
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == "__main__":
    logging.basicConfig()
    serve()
