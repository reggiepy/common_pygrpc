# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/11/15 15:57

import glob
from os import path
from pathlib import Path

from Cython.Build import cythonize
from setuptools import setup, find_packages
from wheel.bdist_wheel import bdist_wheel

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


# python setup.py sdist 打包成tar.gz的形式
# python setup.py bdist_wheel  打包成wheel格式
# 文件名：setuptools_myplugin.py


class MyPluginCommand(bdist_wheel):
    """Custom command to print a message."""

    def egg2dist(self, egginfo_path, distinfo_path):
        result = super().egg2dist(egginfo_path, distinfo_path)
        for file in glob.glob("src/*/*pyi"):
            f = Path(file)
            d = Path(self.bdist_dir).joinpath(self.distribution.get_name()).joinpath(f"{f.name}")
            print(f"copying {f} >>>>>>> {d}")
            d.write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
        return result

    def run(self):
        super().run()


setup(
    name="common_pygrpc",
    version="1.0.0",
    description="common python grpc service",
    author="reggiepy",
    author_email="reggiepy@foxmail.com",
    url="https://github.com/reggiepy/common_pygrpc",
    license="LICENSE",
    # --------------------------------------- <<< 使用C 编译 -----------------------------------------
    # cmdclass={
    #     'bdist_wheel': MyPluginCommand,
    # },
    # --------------------------------------- 使用C 编译 >>> -----------------------------------------
    package_dir={"": "src"},
    # --------------------------------------- <<< 使用源码 -----------------------------------------
    # # # 包含pyi文件
    # package_data={"": ["src/*/*pyi"]},
    # py_modules=['common_pygrpc'],
    # packages=find_packages(where="src"),
    # --------------------------------------- 使用源码 >>> -----------------------------------------
    install_requires=["grpcio==1.50.0", "protobuf==3.20.3"],
    python_requires=">=3.6",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    # --------------------------------------- <<< 使用C 编译 -----------------------------------------
    ext_modules=cythonize(
        [
            "src/common_pygrpc/grpclib.py",
            "src/common_pygrpc/common_pb2.py",
            "src/common_pygrpc/common_pb2_grpc.py",
        ],
        compiler_directives={"language_level": 3},
    ),
    # --------------------------------------- 使用C 编译 >>> -----------------------------------------
)
