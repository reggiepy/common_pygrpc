# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/11/15 15:35

from grpclib import *


@grpc_service(server='test')
def say(count, message):
    pass


@grpc_service(server='test')
def error():
    pass