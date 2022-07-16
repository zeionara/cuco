from dataclasses import dataclass

from cuco import config_parser

from .Foo import Foo


@config_parser()
@dataclass
class Bar(Foo):
    baz: list
