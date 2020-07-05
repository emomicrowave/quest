import yaml
import xdg
from dataclasses import dataclass, field
from typing import Dict
from pathlib import Path


@dataclass
class Configuration:
    path: str = field(default=xdg.XDG_DATA_HOME / "quest/tasks.yaml")
    trello: Dict = field(default_factory=dict)
    taskfile: Path = field(default=xdg.XDG_DATA_HOME / "quest/taskfile")
    config: Path = field(default=xdg.XDG_CONFIG_HOME / "quest.yaml")

    def __post_init__(self):
        self.path = Path(self.path).expanduser()
        if self.taskfile:
            self.taskfile = Path(self.taskfile).expanduser()


def load_user_configuration() -> Configuration:
    config_path = xdg.XDG_CONFIG_HOME / "quest.yaml"
    if config_path.exists():
        with open(config_path, "r") as f:
            config = yaml.load(f, Loader=yaml.Loader)
            return Configuration(**config)
    else:
        return Configuration()
