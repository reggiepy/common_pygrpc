from _typeshed import Incomplete

class CommonServiceStub:
    handle: Incomplete
    def __init__(self, channel) -> None: ...

class CommonServiceServicer:
    def handle(self, request, context) -> None: ...

def add_CommonServiceServicer_to_server(servicer, server) -> None: ...

class CommonService:
    @staticmethod
    def handle(request, target, options=..., channel_credentials: Incomplete | None = ..., call_credentials: Incomplete | None = ..., insecure: bool = ..., compression: Incomplete | None = ..., wait_for_ready: Incomplete | None = ..., timeout: Incomplete | None = ..., metadata: Incomplete | None = ...): ...
