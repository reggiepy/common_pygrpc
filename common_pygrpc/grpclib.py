#!/usr/bin/python
# -*- coding: UTF-8 -*-

import functools
import importlib
import inspect
import json
import logging
import sys
import time
import traceback
import uuid
from concurrent import futures

import common_pb2
import common_pb2_grpc
import grpc
from google.protobuf import json_format

logger = logging.getLogger(__name__)
rpc_logger = logging.getLogger("rpc_log")


def rpc_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        response = func(*args, **kwargs)
        process_time = time.time() - start_time
        func_name = "{}.{}".format(func.__module__, func.__name__)
        sig = inspect.signature(func)
        bind = sig.bind(*args, **kwargs).arguments
        request = bind.get("request")
        json_data = json_format.MessageToJson(response, preserving_proto_field_name=True)
        if len(json_data) > 1024 * 4:
            rpc_logger.debug("{}".format({
                "type": "rpc_log",
                "request_id": request.request_id,
                "function": func_name,
                "process_time": "{:.6f}s".format(process_time),
                "response": json_data[:1024 * 4] + "...",
            }))
        else:
            rpc_logger.debug("{}".format({
                "type": "rpc_log",
                "request_id": request.request_id,
                "function": func_name,
                "status": response.status,
                "process_time": "{:.6f}s".format(process_time),
                "response": json.loads(json_data),
            }))
        return response

    return wrapper


class Server:

    def __init__(self, server, host, port):
        self.server = server
        self.host = host
        self.port = port
        self.addr = host + ':' + str(port)
        self._channel = None

    def copy(self):
        return type(self)(self.server, self.host, self.port)

    @property
    def channel(self):
        if self._channel is None:
            self._channel = grpc.insecure_channel(self.addr)
        return self._channel

    def __enter__(self):
        stub = common_pb2_grpc.CommonServiceStub(self.channel)
        return stub

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.channel.close()


class CommonService(common_pb2_grpc.CommonServiceServicer):

    @classmethod
    def clazz_handler(cls, clazz):
        return clazz

    @rpc_log
    def handle(self, request, context):
        request_str = request.request.decode('utf-8')
        grpc_request = json.loads(request_str)
        response = {
            'status': 0,
            'message': "",
            'excType': "",
            'result': {
                "status": "",
                "msg": "",
                "data": "",
            },
        }
        clazz = grpc_request.get('clazz')
        _clazz = self.clazz_handler(clazz)
        module = importlib.import_module(_clazz)
        method = grpc_request.get('method')
        invoke = functools.reduce(lambda x, y: getattr(x, y), [module, *method.split('.')])
        args = grpc_request.get('args') or ()
        kwargs = grpc_request.get('kwargs') or {}
        try:
            response['result'] = invoke(*args, **kwargs)
        except Exception as e:
            exc_type, exc_value, exc_tb = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_tb)
            response['status'] = -1
            response['message'] = str(e)
            response['excType'] = exc_type.__name__

        return common_pb2.CommonResponse(
            response=json.dumps(response, ensure_ascii=False).encode("utf-8"),
            status=response["status"]
        )


class GrpcClient:

    def handle(self):
        pass

    def connect(self, server):
        """
        get server stub
        :param server:
        :return:
        """
        return self.stubs.get(server)

    def get_server(self, server):
        return self.server_address.get(server)

    def load(self, servers):
        """
        load grpc server list
        :param servers: Server
        :return:
        """
        for server in servers:
            channel = grpc.insecure_channel(server.addr)
            stub = common_pb2_grpc.CommonServiceStub(channel)
            self.stubs[server.server] = stub
            self.server_address[server.server] = server

    def __init__(self):
        self.stubs = {}
        self.server_address = {}


class GrpcServer:
    def __init__(self, host='0.0.0.0', port=6565, max_workers=10):
        self.address = host + ':' + str(port)
        self.max_workers = max_workers
        self.service = CommonService()
        self.rpc_server: grpc.server = None

    def set_clazz_handler(self, func):
        if callable(func):
            self.service.clazz_handler = func

    def run(self):
        self.run_blocking()

    def run_background(self):
        self.rpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=self.max_workers))
        common_pb2_grpc.add_CommonServiceServicer_to_server(self.service, self.rpc_server)
        self.rpc_server.add_insecure_port(self.address)
        self.rpc_server.start()
        logger.info('grpc server running, listen on ' + self.address)

    def run_blocking(self):
        self.run_background()
        try:
            while True:
                time.sleep(60 * 60 * 24)
        except KeyboardInterrupt:
            self.rpc_server.stop(0)


class GrpcException(Exception):

    def __init__(self, exc_type, message):
        self.exc_type = exc_type
        self.message = message


def grpc_service(server, serialize=3):
    """
    grpc service define
    :param server: server name
    :param serialize: serialize type, default 3 : json
    :return:
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            sig = inspect.signature(func)
            bind = sig.bind(*args, **kwargs).arguments
            if sig.parameters.get("cls"):
                cls = bind.get("cls")
                bind.pop("cls")
            rpc_client = grpc_client.connect(server)
            response_json = GrpcHelper.call_rpc_result(
                rpc_client,
                clazz=func.__module__,
                method=func.__qualname__,
                args=(),
                kwargs={k: v for k, v in bind.items()},
            )
            return response_json

        return wrapper

    return decorator


class GrpcHelper:
    @classmethod
    def call_rpc(
            cls,
            rpc_client,
            clazz,
            method,
            args=None,
            kwargs=None,
            request_id=None,
            serialize=3
    ):
        """
        common call rpc
        Args:
            rpc_client:
            clazz:
            method:
            args:
            kwargs:
            request_id:
            serialize:

        Returns:

        """
        request_id = request_id if request_id is not None else uuid.uuid4().hex
        args = args if args is not None else ()
        kwargs = kwargs if kwargs is not None else {}
        request = {
            'clazz': clazz,
            'method': method,
            'args': args,
            'kwargs': dict(kwargs),
        }
        request_json = json.dumps(request, ensure_ascii=False)
        resp = rpc_client.handle(
            common_pb2.CommonRequest(
                request=request_json.encode('utf-8'),
                serialize=serialize,
                request_id=request_id
            )
        )

        return resp

    @classmethod
    def call_rpc_result(cls, rpc_client, clazz, method, args=None, kwargs=None, request_id=None):
        resp = cls.call_rpc(
            rpc_client,
            clazz=clazz,
            method=method,
            args=args,
            kwargs=kwargs,
            request_id=request_id,
        )
        status = resp.status
        response = resp.response.decode("utf-8")
        response_json = json.loads(response)
        if response_json.get('status') == 0:
            return response_json.get('result')
        elif status == -1 or response_json.get('status') == -1:
            raise GrpcException(response_json.get('excType'), response_json.get('message'))
        else:
            raise Exception('unknown grpc exception')


grpc_client = GrpcClient()
