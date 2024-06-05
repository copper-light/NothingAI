from rest_framework import status


class Message:

    """
    응답 전문에 대한 메시지 관리 (향후 DB로 전환 필요?)
    """

    # ERROR Messages
    INVALID_REQUIRED_FIELD = "'{}' is a required field"
    INVALID_BLANK_FILED = "'{}' should not be blank"
    INVALID_MAX_VALUE = "'{}' is not within a valid range"
    FAILED_TO_UPLOAD_FILES = "Failed to upload files"
    INVALID_RUN_FILE = "Run file not found ({})"
    INVALID_REQUIRED_FILES = "Files for upload are required"
    INVALID_FILE_PATH = "'{}' is an invalid path"
    FILE_EXISTS = "{} : File already exists"
    NOT_FOUND_FILE = "{} : No such file or directory"
    NOT_EXISTS = "{} is not exists"
    INVALID_CODE = "'{}' is not a valid. The value must be one of [{}]"


class HTTPMessage:
    msg = {
        status.HTTP_200_OK: "OK",
        status.HTTP_400_BAD_REQUEST: "Bad request",
        status.HTTP_404_NOT_FOUND: "Resource not found",
        status.HTTP_500_INTERNAL_SERVER_ERROR: "Internal server error"
    }

    @classmethod
    def get(cls, code: int):
        if code in cls.msg:
            return cls.msg[code]
        else:
            return None
