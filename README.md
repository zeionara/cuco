<p align="center">
    <img src="assets/logo.png"/>
</p>

# CuCo

CuCo (**Cu**te **Co**nfiguration) is a project for making it easier to write configuration files which may be automatically converted into a set of alternative system setups.

## Installation

To install the package, execute the following command:

```sh
pip install cuco
```

## Usage

To use the package, first, annotate some of your classes with annotator `config_parser` according to the following example:

```py
from dataclasses import dataclass
from cuco import config_parser, Config

@config_parser()
@dataclass
class Foo(Config):
    bar: int = 0
    baz: str = None

    name: str = None  # This field contains configuration name, which includes values for alternating configuration fields in a particular setup
```

Then you would need to create a file with name `assets/types/foo.yml` for this class with specification of keys which are allowed to set up in this file (the following example demonstrates that field `qux` from configuration file will be translated into the field `bar` of the generated objects):

```yaml
qux: bar
```

After that you finally can create a file with name `assets/foo/default.yml` with some value for the configurable fields (the given example demonstrates array consisting of 2 values, which will lead to generation of 2 config objects):

```yaml
_type: foo

qux:
    - 1
    - 2
```

The last step is calling method `make_configs` which will read all the configuration files and decide how they should be parsed, returning the list of generated configuration objects:

```py
from .Foo import Foo

configs = make_configs(
    path = 'assets/foo/default.yml', type_specification_root = 'assets/types'
)
```

## Testing

To run the tests, execute the following command:

```sh
python -m unittest discover test
```
