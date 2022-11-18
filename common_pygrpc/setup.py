# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/11/15 15:57

from os import path

from setuptools import setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# python setup.py sdist 打包成tar.gz的形式
# python setup.py bdist_wheel  打包成wheel格式
setup(
    name='common-pygrpc',
    version='0.0.1',
    description='common python grpc service',
    author='reggiepy',
    author_email='reggiepy@foxmail.com',
    url='https://github.com/reggiepy/grpcTest',
    py_modules=['grpclib', 'common_pb2', 'common_pb2_grpc'],
    install_requires=['grpcio>=1.50.0', 'protobuf>=3.20.3'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
