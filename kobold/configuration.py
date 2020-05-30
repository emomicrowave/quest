import yaml
import xdg
from dataclasses import dataclass, field
from typing import Dict
from pathlib import Path


defaults = {
    "path": "~/.kobold.yaml",
    "trello": {},
}


@dataclass
class Config:
    path: str
    trello: Dict
    taskfile: Path = None

    def __post_init__(self):
        self.path = Path(self.path).expanduser()
        if self.taskfile:
            self.taskfile = Path(self.taskfile).expanduser()


def load_user_configuration() -> Config:
    config_path = xdg.XDG_CONFIG_HOME / "kobold.yaml"
    with open(config_path, "r") as f:
        config = yaml.load(f, Loader=yaml.Loader)
    return Config(**{**defaults, **config})
