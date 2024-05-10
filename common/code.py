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
    def __init__(self):
        self.item = {}
        for key in self.__class__.__dict__.keys():
            value = str(self.__class__.__dict__[key])
            self.item[value] = getattr(self.__class__, key)

    def __str__(self):
        return self.__class__.__name__.replace("_", " ")

    def __getitem__(self, index):
        return self.item[str(index)]


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


class RUN_ENV_TYPE(C):
    LOCAL      = E("Local",      0)
    DOCKER     = E("Docker",     1)
    KUBERNETES = E("Kubernetes", 2)


class TASK_STATUS(C):
    WAIT    = E("Wait",    0)
    PREPARE = E("Prepare", 1)
    RUNNING = E("Running", 2)
    DONE    = E("Done",    3)
    FAILED  = E("Failed",  4)


class PYTHON_VERSION(C):
    PYTHON3_6 = E("python3.6", 0)
    PYTHON3_7 = E("python3.7", 1)
    PYTHON3_8 = E("python3.8", 2)
    PYTHON3_9 = E("python3.9", 3)
    PYTHON3_10 = E("python3.10", 4)
    PYTHON3_11 = E("python3.11", 5)
    PYTHON3_12 = E("python3.12", 6)


if __name__ == "__main__":
    a = PYTHON_VERSION()

    print(a[1].name)

