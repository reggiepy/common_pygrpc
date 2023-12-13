# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/11/15 15:35

from grpclib import *


@grpc_service(server='test')
def say(i, message):
    pass


@grpc_service(server='test')
def error():
    pass


class User:
    @classmethod
    @grpc_service(server='test')
    def create(cls, name):
        pass

    @staticmethod
    @grpc_service(server='test')
    def get2(name):
        pass


class B:
    def __init__(self):
        pass

    def get(self):
        pass
