# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/11/15 15:36
def say(i, message):
    print(str(i) + ':' + message)
    return 'received id :' + str(i)


def error():
    x = 1 / 0
    return 'error'


class User:
    @classmethod
    def create(cls, name):
        return name

    @staticmethod
    def get2(name):
        return name


class B:
    def __init__(self, a: int, b: int, c: int):
        self.name = "wttt"
        self.a = a
        self.b = b
        self.c = c

    def get(self):
        return f"{self.name} {self.a} {self.b} {self.c}"


if __name__ == '__main__':
    import inspect

    members = inspect.getmembers(B)
    for member in members:
        func_name, func_type = member
        if inspect.isfunction(func_type):
            print(func_type.__qualname__)
            sig = inspect.signature(getattr(B, func_name))
            print(sig.parameters)
            print(func_name, func_type)

    b = B(1, 2, 3)
    sig = inspect.signature(B)
    print(sig.parameters)
    for k, v, in sig.parameters.items():
        print(k, v.annotation)

    User.create("fasdf")
