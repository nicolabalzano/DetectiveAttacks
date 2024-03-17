def convert_lists_to_tuples_in_init(cls):
    original_init = cls.__init__

    def __init__(self, *args, **kwargs):
        new_kwargs = {k: tuple(v) if isinstance(v, list) else v for k, v in kwargs.items()}
        original_init(self, *args, **new_kwargs)

    cls.__init__ = __init__
    return cls