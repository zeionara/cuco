from dataclasses import dataclass

from cuco import config_parser, Config


@config_parser()
@dataclass
class Garply(Config):
    foo: str
    bar: str

    name: str
