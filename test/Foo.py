from dataclasses import dataclass

from cuco import config_parser, Config


@config_parser()
@dataclass
class Foo(Config):
    foo: int
    bar: str

    name: str
