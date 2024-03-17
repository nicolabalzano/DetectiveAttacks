from dataclasses import dataclass


@dataclass
class MySTIXBase20:
    def __init__(self, obj):
        self.obj = obj