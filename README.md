# python3 

[![python version](https://img.shields.io/badge/python-3.7-success.svg?style=flat)](https://github.com/reggiepy/common-pygrpc)
[![release](https://img.shields.io/github/v/tag/reggiepy/common-pygrpc?color=success&label=release)](https://github.com/reggiepy/common-pygrpc)
[![build status](https://img.shields.io/badge/build-pass-success.svg?style=flat)](https://github.com/reggiepy/common-pygrpc)
[![License](https://img.shields.io/badge/license-GNU%203.0-success.svg?style=flat)](https://github.com/reggiepy/common-pygrpc)

## Installation

```bash
git clone https://github.com/reggiepy/common-pygrpc.git
cd common-pygrpc
```

## Usage

```bash
# 打包成 wheel
python setup.py bdist_wheel

# run in client server
python client.py
# run in server server
python server.py

# 生成 python rpc
python -m grpc_tools.protoc -I proto --python_out=lib --grpc_python_out=lib common.proto
# 生成 js rpc
protoc  -I proto common.proto --js_out=import_style=commonjs:lib --grpc-web_out=import_style=commonjs,mode=grpcwebtext:lib
# 生成 golang rpc
protoc  -I proto common.proto --go_out=plugins=grpc:lib
```

## Install

```bash
pip install common_pygrpc-0.0.1-py3-none-any.whl --force
```

## Architecture
