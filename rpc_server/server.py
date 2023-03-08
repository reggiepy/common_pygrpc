# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/11/15 15:37
from grpclib import GrpcServer

if __name__ == '__main__':
    server = GrpcServer()
    server.set_clazz_handler(lambda x: x.replace('rpc_client', "rpc_server"))
    server.run_background()
    import time
    while True:
        time.sleep(60 * 60 * 24)
