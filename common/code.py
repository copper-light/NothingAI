from common.enum import E, C


class MODEL_TYPE(C):
    CLASSIFICATION   = E("classification",  0)
    REGRESSION       = E("regression",      1)
    OBJECT_DETECTION = E("object_detection",2)
    SEGMENTATION     = E("segmentation",    3)
    ETC              = E("etc",             99)


class DATASET_TYPE(C):
    UNKNOWN = E("unknown", 0)
    IMAGE   = E("image",   1)
    SOUND   = E("sound",   2)
    MOVIE   = E("movie",   3)
    CSV     = E("csv",     4)
    ETC     = E("etc",     99)


class STORAGE_TYPE(C):
    LOCAL          = E("local",          0)
    GIT            = E("git",            1)
    OBJECT_STORAGE = E("object",         2)


class VISIBILITY(C):
    PUBLIC   = E("public",   0)
    INTERNAL = E("internal", 1)
    PRIVATE  = E("private",  2)


class RUN_ENV_TYPE(C):
    LOCAL      = E("local",      0)
    DOCKER     = E("docker",     1)
    KUBERNETES = E("kubernetes", 2)


class TASK_STATUS(C):
    WAIT    = E("wait",    0)
    PREPARE = E("prepare", 1)
    RUNNING = E("running", 2)
    DONE    = E("done",    3)
    FAILED  = E("failed",  4)


class PYTHON_VERSION(C):
    PYTHON3_6  = E("python3.6", 0)
    PYTHON3_7  = E("python3.7", 1)
    PYTHON3_8  = E("python3.8", 2)
    PYTHON3_9  = E("python3.9", 3)
    PYTHON3_10 = E("python3.10", 4)
    PYTHON3_11 = E("python3.11", 5)
    PYTHON3_12 = E("python3.12", 6)


class HYPER_PARAM_TYPE(C):
    NORMAL            = E("normal",            0)
    ARRAY             = E("array",             1)
    GRID_SEARCH       = E("grid_search",       2)
    RANDOMIZED_SEARCH = E("randomized_search", 3)


# if __name__ == "__main__":
#     print(MODEL_TYPE[0])
#     print(MODEL_TYPE["classification"].name)
#
#     if 'local' in STORAGE_TYPE.keys():
#         print("local")
#     else:
#         print("not found")
