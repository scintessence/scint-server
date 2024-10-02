from scint.framework.state.metadata import collector
from scint.framework.types.base import BaseType
from scint.framework.state.state import State
from scint.framework.types.composition import CompositionType


class StateType(BaseType):
    def __new__(cls, name, bases, dct, **kwds):
        def _index(self):
            for key, value in self.state.items():
                print(key)

        def _parse(self, obj):
            for key, value in obj.items():
                if key == "labels" and value is not None:
                    self.labels.add(item for item in value)

        def _calculate(self, obj):
            for key, value in obj.items():
                if key == "embedding" and value is not None:
                    self.embeddings.append(value)
                    self.embedding = [sum(e) / len(e) for e in zip(self.embeddings)]

        dct["_type"] = kwds.get("type")
        dct["_index"] = _index
        dct["_parse"] = _parse
        dct["_calculate"] = _calculate
        dct["_call_stack"] = []
        for key, value in dct.items():
            if callable(value) and not key.startswith("__"):
                if callable(value):
                    dct[key] = collector(value)
                elif not isinstance(value, State):
                    dct[key] = State()

        return super().__new__(cls, name, bases, dct)


class Composition(metaclass=CompositionType):
    def __init__(self, *args, **kwargs):
        for item in args:
            setattr(self, type(item).__name__.lower(), item)
        for key, value in kwargs.items():
            setattr(self, key, value)
