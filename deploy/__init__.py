from . import *

from os import makedirs
from typing import Callable
from pathlib import Path


class DeployBase:
    output: Path = Path(Path(__file__).parent.parent, "output")
    path: Path
    predict: Callable

    def __init__(self, *args, **kwargs):
        makedirs(self.output, exist_ok=True)
        super().__init__(*args, **kwargs)

    def test_deploy(self):
        raise NotImplementedError(
            f"Не определен метод `test_deploy` в классе `{self.__class__.mro()[1].__name__}`"
        )


class DeployImageSegmentation(DeployBase):
    def test_deploy(self):
        self.predict(
            str(Path(self.path, "preset", "in", "1.jpg").absolute()),
            str(Path(self.output, f"{self.__class__.__name__}.jpg")),
        )


class DeployImageClassification(DeployBase):
    def test_deploy(self):
        self.predict(str(Path(self.path, "1.jpg").absolute()))
