from dataclasses import dataclass

from cuco import config_parser, Config


@config_parser(module_name = 'foo.corge')
@dataclass
class Corge(Config):
    foo: int
    name: str = None
