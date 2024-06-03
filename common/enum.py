from django.db.migrations.serializer import BaseSerializer
from django.db.migrations.writer import MigrationWriter


class E:

    def __init__(self, name, code):
        self.__name = name
        self.__code = code

    @property
    def code(self):
        return self.__code

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @code.setter
    def code(self, value):
        self.__code = value

    def __str__(self):
        return str(self.__code)

    def __int__(self):
        return int(self.__code)

    def __repr__(self):
        return self.__code.__repr__()

    def __eq__(self, other):
        return other == self.__code

    def __ge__(self, other):
        return other >= self.__code

    def __le__(self, other):
        return other <= self.__code

    def __gt__(self, other):
        return other > self.__code

    def __lt__(self, other):
        return other < self.__code


class C:
    sub_class = {}
    sub_names = {}
    sub_codes = {}

    @classmethod
    def _create_item(cls):
        cls.sub_class[cls.__name__] = {}
        cls.sub_names[cls.__name__] = list()
        cls.sub_codes[cls.__name__] = list()
        for key in cls.__dict__.keys():
            value = cls.__dict__[key]
            if key not in ('__module__', '__doc__'):
                cls.sub_class[cls.__name__][value.code] = value.name
                cls.sub_class[cls.__name__][value.name] = value.code
                cls.sub_names[cls.__name__].append(value.name)
                cls.sub_codes[cls.__name__].append(value.code)
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

    @classmethod
    def keys(cls):
        if cls.__name__ not in cls.sub_class:
            cls._create_item()
        return cls.sub_class[cls.__name__].keys()

    @classmethod
    def names(cls):
        if cls.__name__ not in cls.sub_class:
            cls._create_item()
        return cls.sub_names[cls.__name__]

    @classmethod
    def codes(cls):
        if cls.__name__ not in cls.sub_class:
            cls._create_item()
        return cls.sub_codes[cls.__name__]


# DB Migration 에 필요한 클래스
class ESerializer(BaseSerializer):
    def serialize(self):
        return repr(self.value), {"from common.code import E"}


MigrationWriter.register_serializer(E, ESerializer)
