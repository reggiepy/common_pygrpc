from rpc_client.hello.test import *

servers = [Server('test', '127.0.0.1', 6565)]
grpc_client.load(servers)

response = say(1, 'hello grpc!')
print(response)

response = User.create("wt")
print(response)

response = User.get2("wtfafsfsfas")
print(response)

response = error()
print(response)
