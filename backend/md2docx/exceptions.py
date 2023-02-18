import json
import re
from enum import Enum
from typing import Any, Optional


class MetadataValidationErrorType(str, Enum):
    UNKNOWN_KEY = 'unknown_key'
    WRONG_VALUE_TYPE = 'wrong_value_type'


class ProcessingError(Exception):
    """Error raised during processing"""
    pass


class WinProcessingError(Exception):
    """Error raised during windows processing"""
    pass


class PostProcessingError(Exception):
    """Error raised during post-processing"""
    pass


class MetadataValidationErrorItem:
    def __init__(self, key: str, err_type: MetadataValidationErrorType):
        self.key = key
        self.err_type = err_type

    def __iter__(self):
        return iter((self.key, self.err_type))


class MetadataValidationError(Exception):
    def __init__(self, errors: list[MetadataValidationErrorItem], *args):
        super().__init__(*args)
        self.errors = errors

    def _get_error_message(self, key: str, type: MetadataValidationErrorType) -> str:
        if type == MetadataValidationErrorType.UNKNOWN_KEY:
            return "Unknown metadata"
        else:
            return "Wrong value type"

    def __str__(self) -> str:
        message = []

        for key, err_type in self.errors:
            error_dict = {
                'key': key,
                'type': err_type.value,
                'message': self._get_error_message(key, err_type)
            }
            message.append(error_dict)

        # Serializing errors
        return json.dumps(message)
