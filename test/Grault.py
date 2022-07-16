from dataclasses import dataclass

from test.Corge import Corge

from cuco import config_parser, Config


@config_parser(module_name = 'bar.baz.grault')
@dataclass
class Grault(Config):
    bar: int
    baz: Corge

    name: str
