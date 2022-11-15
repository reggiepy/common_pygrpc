# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/11/15 11:12
# hello_server.py

import grpc
from concurrent import futures


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 绑定处理器
    server.add_insecure_port('[::]:50054')
    server.start()
    print('gRPC 服务端已开启，端口为50054...')
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
