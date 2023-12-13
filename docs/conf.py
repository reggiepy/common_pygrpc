# *_*coding:utf-8 *_*
# @Author : Reggie
# @Time : 2023/12/11 15:24
import importlib
from datetime import datetime

import tomllib

with open("../pyproject.toml", "rb") as f:
    pyproject = tomllib.load(f)

project = pyproject["project"]["name"]
conf = {"module": project.replace("-", "_")}

try:
    conf.update(pyproject["tool"]["sphinx"]["x-conf"])
except KeyError:
    pass

module = importlib.import_module(conf["module"])
release = module.__version__
version = ".".join(release.split(".")[:2])
author = ", ".join(author["name"] for author in pyproject["project"]["authors"])
year = datetime.now().year
copyright = f"{year}, {author}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx_mdinclude",
]

htmlhelp_basename = f"{project}-doc"
html_theme = "furo"
pygments_style = "sphinx"