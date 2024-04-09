from enum import Enum


class OperationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCECSS = "success"
    FAILED = "failed"
