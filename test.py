import deploy

from os import listdir
from sys import modules
from json import load as json_load
from pathlib import Path
from pkgutil import iter_modules
from unittest import TestCase
from importlib import import_module


deploy_path = Path(Path(__file__).parent, "deploy")

for item in listdir(deploy_path):
    item_path = Path(deploy_path, item)
    if item == "__pycache__" or not item_path.is_dir():
        continue
    Path(item_path, "__init__.py").touch()

for item in iter_modules([deploy_path]):
    with open(Path(deploy_path, item.name, "config.json")) as config_ref:
        config = json_load(config_ref)
        classextra = getattr(deploy, f'Deploy{config.get("type")}')
        classname = f"Deploy{item.name.title()}"
        setattr(
            modules.get(__name__),
            classname,
            type(
                classname,
                (classextra, TestCase),
                {
                    "path": Path(deploy_path, item.name),
                    "predict": staticmethod(
                        import_module(f"deploy.{item.name}.script").predict
                    ),
                },
            ),
        )
