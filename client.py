# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/11/15 13:33

import grpc

# For more channel options, please see https://grpc.io/grpc/core/group__grpc__arg__keys.html
DEFAULT_GRPC_OPTIONS = (
    ("grpc.enable_retries", 0),
    ("grpc.keepalive_timeout_ms", 1000),
    ("grpc.grpclb_call_timeout_ms", 500),
    ("grpc.grpclb_fallback_timeout_ms", 1000),
    ("grpc.priority_failover_timeout_ms", 1000),
    ("grpc.server_handshake_timeout_ms", 1000),
    ("grpc.client_idle_timeout_ms", 1000),
    ("grpc.max_send_message_length", 256 * 1024 * 1024),
    ("grpc.max_receive_message_length", 256 * 1024 * 1024),
)


class RpcClient:
    def __init__(self, host="localhost", port=8081, grpc_options=DEFAULT_GRPC_OPTIONS, compression=None):
        """创建RPC客户端
        @param host: 主机地址
        @param port: 主机端口
        @param grpc_options: grpc配置参数
        @param compression: 是否启用数据压缩
        """
        self.target = "{}:{}".format(host, port)
        self._channel = grpc.aio.insecure_channel(target=self.target, options=grpc_options, compression=compression, )
        super().__init__(self._channel)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._channel.close()
        self._channel = None

    async def close(self):
        if self._channel:
            await self._channel.close()
