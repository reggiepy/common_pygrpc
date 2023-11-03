# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/11/15 15:57

from os import path
from Cython.Build import cythonize
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# python setup.py sdist 打包成tar.gz的形式
# python setup.py bdist_wheel  打包成wheel格式


setup(
    name='common_pygrpc',
    version='0.0.5',
    description='common python grpc service',
    author='reggiepy',
    author_email='reggiepy@foxmail.com',
    url='https://github.com/reggiepy/common_pygrpc',
    license="LICENSE",
    # py_modules=['grpclib', 'common_pb2', 'common_pb2_grpc'],
    install_requires=['grpcio==1.50.0', 'protobuf==3.20.3'],
    python_requires='>=3.6',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    ext_modules=cythonize(['grpclib.py', 'common_pb2.py', 'common_pb2_grpc.py'], compiler_directives={'language_level': 3}),
)
