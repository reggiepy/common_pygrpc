# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2022/11/18 14:29
import argparse
import configparser
import ctypes
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

# ############################################ Tools ##################################################################

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12
FOREGROUND_BLACK = 0x0
FOREGROUND_BLUE = 0x01  # text color contains blue.
FOREGROUND_GREEN = 0x02  # text color contains green.
FOREGROUND_RED = 0x04  # text color contains red.
FOREGROUND_INTENSITY = 0x08  # text color is intensified.
BACKGROUND_BLUE = 0x10  # background color contains blue.
BACKGROUND_GREEN = 0x20  # background color contains green.
BACKGROUND_RED = 0x40  # background color contains red.
BACKGROUND_INTENSITY = 0x80  # background color is intensified.


class Color:
    """ See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winprog/winprog/windows_api_reference.asp
    for information on Windows APIs.
    """
    std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    def set_cmd_color(self, color, handle=std_out_handle):
        """(color) -> bit
        Example: set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE | FOREGROUND_INTENSITY)
        """
        # Chemical Engineering Design Library (ChEDL). Utilities for process modeling.
        bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return bool

    def reset_color(self):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

    def print_red_text(self, print_text):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY)
        print(print_text)
        self.reset_color()

    def print_green_text(self, print_text):
        self.set_cmd_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
        print(print_text)
        self.reset_color()

    def print_blue_text(self, print_text):
        self.set_cmd_color(FOREGROUND_BLUE | FOREGROUND_INTENSITY)
        print(print_text)
        self.reset_color()

    def print_red_text_with_blue_bg(self, print_text):
        self.set_cmd_color(FOREGROUND_RED | FOREGROUND_INTENSITY | BACKGROUND_BLUE | BACKGROUND_INTENSITY)
        print(print_text)
        self.reset_color()


# clr = Color()


# clr.print_red_text('red')
# clr.print_green_text('green')
# clr.print_blue_text('blue')
# clr.print_red_text_with_blue_bg('background')

class Color2:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def print_red_text(self, print_text):
        print(self.FAIL + print_text + self.ENDC)

    def print_green_text(self, print_text):
        print(self.OKGREEN + print_text + self.ENDC)

    def print_blue_text(self, print_text):
        print(self.OKBLUE + print_text + self.ENDC)


# clr2 = Color2()

# clr2.print_red_text('red')
# clr2.print_green_text('green')
# clr2.print_blue_text('blue')


def run_command(cmd, shell=False, env=None):
    if shell:
        if isinstance(cmd, (list, tuple)):
            real_cmd = " ".join([str(i) for i in cmd])
        else:
            raise RuntimeError("cmd type not support")
    else:
        if isinstance(cmd, str):
            real_cmd = shlex.split(cmd)
        elif isinstance(cmd, (list, tuple)):
            real_cmd = [str(i) for i in cmd]
        else:
            raise RuntimeError("cmd type not support")
    if isinstance(real_cmd, (tuple, list)):
        print(" ".join(real_cmd))
    else:
        print(real_cmd)

    p = subprocess.Popen(
        real_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        shell=shell
    )
    out, err = p.communicate()
    rc = p.returncode
    return out, err, rc


def decode_bytes(bytes_str):
    code = ["utf-8", "gbk"]
    for c in code:
        try:
            return bytes_str.decode(c)
        except UnicodeDecodeError:
            continue


class Config:
    def __init__(self):
        self.config_path = Path("build_pyd.ini")
        self.config = configparser.ConfigParser(
            defaults={
                'clear_build_dir': 'True',
                'base_path': 'domain',
                'color_module': 'Color2',
                'dist_path': 'dist',
                'dist_name': 'domain',
                'rm_c_file': 'True',
            },
            default_section="Common",
        )
        if self.config_path.exists():
            self.config.read("build_pyd.ini", encoding="utf-8")

    def _convert_to_boolean(self, value):
        """Return a boolean value translating from other types if necessary.
        """

        if value.lower() not in self.config.BOOLEAN_STATES:
            raise ValueError('Not a boolean: %s' % value)
        return self.config.BOOLEAN_STATES[value.lower()]

    @staticmethod
    def _convert_to_list(value):
        return value.split(",")

    def parse(self):
        translate_value = {
            "clear_build_dir": self._convert_to_boolean,
        }
        result = {}
        for section in self.config.sections():
            for k, v in self.config.items(section):
                print(k, v)
                if k in translate_value:
                    v = translate_value[k](v)
                result[k] = v
        return result


# ########################################### 实现 ###############################################################

class Version:
    VERSION_NB_COMPILE = re.compile(r"^\d+\.\d+\.\d+$")

    @classmethod
    def current_version(cls, setup_file):
        version_compile = re.compile(r".*?version=\'(\d\.\d\.\d)\'.*")
        with open(setup_file, "r", encoding="utf-8") as f:
            for line in f.readlines():
                if "version" in line:
                    match = version_compile.match(line)
                    if match:
                        return match.group(1)
            raise ValueError("can't find version'")

    @classmethod
    def next_version(cls, setup_file):
        current_version = cls.current_version(setup_file)
        next_version = list(map(lambda x: int(x), current_version.split('.')))
        next_version[-1] += 1
        return ".".join(map(lambda x: str(x), next_version))

    @classmethod
    def prev_version(cls, setup_file):
        current_version = cls.current_version(setup_file)
        next_version = list(map(lambda x: int(x), current_version.split('.')))
        next_version[-1] -= 1
        return ".".join(map(lambda x: str(x), next_version))

    @classmethod
    def change_setup_version(cls, setup_file, version=None):
        current_version = cls.current_version(setup_file)
        next_version = version or cls.next_version(setup_file)
        with open(setup_file, "r", encoding="utf-8") as f:
            data = f.read().replace(f"version='{current_version}", f"version='{next_version}")
        with open(setup_file, "w", encoding="utf-8") as f:
            f.write(data)


if __name__ == '__main__':
    BASE_DIR = os.getcwd()
    model_name = "common_pygrpc"
    model_path = Path(BASE_DIR).joinpath(model_name)
    setup_file = model_path.joinpath("setup.py")
    parser = argparse.ArgumentParser(description="whl build script")
    parser.add_argument(
        "-v", "--version", type=str, default="=",
        help="build whl version (= (pass) | + (increase) | new version)"
    )
    parser.add_argument(
        "-t", "--test", type=bool, default=False,
        help="test parameters not generate whl"
    )
    parser.add_argument(
        "-c", "--clean", type=bool, default=True,
        help="clean build directory"
    )
    parser.add_argument(
        "--color_module", type=str, default="Color",
        help="start build"
    )
    args = parser.parse_args()
    if args.test is False:
        # handle color module
        if args.color_module not in globals():
            color_module = Color()
        else:
            color_module = globals().get(args.color_module)()

        # handle version
        color_module.print_green_text(f"current version: {Version.current_version(setup_file)}")

        if args.version != "=":
            if args.version == "+":
                next_version = Version.next_version(setup_file)
            elif args.version == "-":
                next_version = Version.prev_version(setup_file)
            else:
                next_version = args.version
            # match version number
            if Version.VERSION_NB_COMPILE.match(next_version):
                color_module.print_green_text(f"new version: {Version.current_version(setup_file)}")
                # change version
                Version.change_setup_version(setup_file, next_version)

        cmd = f"{Path(sys.executable).as_posix()}" \
              f" -m grpc_tools.protoc " \
              f"-Iproto " \
              f"--python_out=common_pygrpc " \
              f"--grpc_python_out=common_pygrpc  " \
              f"proto/common.proto"
        out, err, rc = run_command(cmd, env={k: v for k, v in os.environ.items()})
        if rc != 0:
            color_module.print_red_text(f"build proto error: {decode_bytes(err)}")
            Version.change_setup_version(setup_file)
        else:
            color_module.print_green_text(f"build proto success: {decode_bytes(out)}")

        os.chdir(Path(BASE_DIR).joinpath(model_name))
        cmd = f"{Path(sys.executable).as_posix()} setup.py bdist_wheel"
        out, err, rc = run_command(cmd, env={k: v for k, v in os.environ.items()})
        if rc != 0:
            color_module.print_red_text(f"build error: {decode_bytes(err)}")
            Version.change_setup_version(setup_file)
        else:
            color_module.print_green_text(f"build success: {decode_bytes(out)}")

        os.chdir(BASE_DIR)
        if args.clean and rc == 0:
            color_module.print_blue_text(f"clean....")
            shutil.rmtree(model_path.joinpath("build"))
            shutil.rmtree(model_path.joinpath(f"{model_name}.egg-info"))
            for file in os.listdir(model_path.joinpath("dist"))[:1]:
                shutil.move(
                    model_path.joinpath("dist").joinpath(file),
                    Path(BASE_DIR).joinpath(file)
                )
            shutil.rmtree(model_path.joinpath("dist"))
            color_module.print_green_text(f"clean success")
    print(args)
