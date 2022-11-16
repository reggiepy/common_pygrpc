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
    def __init__(self, a, b, c):
        self.name = "wttt"
        self.a = a
        self.b = b
        self.c = c

    def get(self):
        return f"{self.name} {self.a} {self.b} {self.c}"


if __name__ == '__main__':
    import inspect

    b = B(1, 2, 3)
    sig = inspect.signature(B)
    print(sig.parameters)
