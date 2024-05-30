from django.db.migrations.serializer import BaseSerializer
from django.db.migrations.writer import MigrationWriter



class E:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return str(self.name)

    def __int__(self):
        return int(self.value)

    def __repr__(self):
        return self.value.__repr__()

    def __eq__(self, other):
        return other == self.value

    def __ge__(self, other):
        return other >= self.value

    def __le__(self, other):
        return other <= self.value

    def __gt__(self, other):
        return other > self.value

    def __lt__(self, other):
        return other < self.value


class C:
    sub_class = {}

    @classmethod
    def _create_item(cls):
        cls.sub_class[cls.__name__] = {}
        for key in cls.__dict__.keys():
            value = cls.__dict__[key]
            if key not in ('__module__', '__doc__'):
                cls.sub_class[cls.__name__][int(value)] = str(value)
                cls.sub_class[cls.__name__][str(value)] = int(value)
            # cls.item[key] = value

    def __str__(self):
        return self.__class__.__name__.replace("_", " ")

    def __class_getitem__(cls, index):
        if cls.__name__ not in cls.sub_class:
            cls._create_item()
        if isinstance(index, str):
            return cls.sub_class[cls.__name__][index]
        else:
            return cls.sub_class[cls.__name__][index]


# DB Migration 에 필요한 클래스
class ESerializer(BaseSerializer):
    def serialize(self):
        return repr(self.value), {"from common.code import E"}


MigrationWriter.register_serializer(E, ESerializer)
