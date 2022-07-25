from .utils.string import substitute_linked_values


class Config:
    @classmethod
    def load(cls, **kwargs):
        substitute_linked_values(kwargs)
        return cls(**kwargs)

    def dump(self) -> dict:
        raise NotImplementedError('Config object serialization is not implemented')
