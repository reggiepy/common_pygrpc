# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/11/15 15:36
def say(i, message):
    print(str(i) + ':' + message)
    return 'received id :' + str(i)


def error():
    x = 1 / 0
    return 'error'