class Config:
    @classmethod
    def load(cls, **kwargs):
        return cls(**kwargs)

    def dump(self) -> dict:
        raise NotImplementedError('Config object serialization is not implemented')
