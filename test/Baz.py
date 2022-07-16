from dataclasses import dataclass

from cuco import config_parser, Config


@config_parser(object_type = 'qux')
@dataclass
class Baz(Config):
    qux: str
    name: str
