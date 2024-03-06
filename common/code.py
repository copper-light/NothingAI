from django.db.migrations.serializer import BaseSerializer
from django.db.migrations.writer import MigrationWriter


class E:

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return str(self.value)

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
    def __str__(self):
        return self.__class__.__name__.replace("_", " ")


class ESerializer(BaseSerializer):
    def serialize(self):
        return repr(self.value), {"from common.code import E"}


MigrationWriter.register_serializer(E, ESerializer)


class MODEL_TYPE(C):
    CLASSIFICATION   = E("Classification",  0)
    REGRESSION       = E("Regression",      1)
    OBJECT_DETECTION = E("Object detection",2)
    SEGMENTATION     = E("Segmentation",    3)
    ETC              = E("ETC",             99)


class DATASET_TYPE(C):
    UNKNOWN = E("Unknown", 0)
    IMAGE   = E("Image",   1)
    SOUND   = E("Sound",   2)
    MOVIE   = E("Movie",   3)
    CSV     = E("CSV",     4)
    ETC     = E("ETC",     99)


class STORAGE_TYPE(C):
    LOCAL          = E("Local",          0)
    GIT            = E("Git",            1)
    OBJECT_STORAGE = E("Object storage", 2)


class VISIBILITY(C):
    PUBLIC   = E("Public",   0)
    INTERNAL = E("Internal", 1)
    PRIVATE  = E("Private",  2)
