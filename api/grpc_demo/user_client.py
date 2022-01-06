#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import logging

import grpc
from api.grpc_demo.rpc_package.userinfo_pb2 import UserInfoRequest, UserInfoReply
from api.grpc_demo.rpc_package.userinfo_pb2_grpc import UserInfoServiceStub


def run():
    # 使用with语法保证channel自动close
    with grpc.insecure_channel('localhost:8881') as channel:
        # 客户端通过stub来实现rpc通信
        stub = UserInfoServiceStub(channel)
        # 客户端必须使用定义好的类型，这里是HelloRequest类型
        response = stub.GetUserInfo(UserInfoRequest(name=''))
    print(response)


if __name__ == "__main__":
    logging.basicConfig()
    run()
