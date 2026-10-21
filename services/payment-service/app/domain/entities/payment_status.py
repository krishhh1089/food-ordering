from enum import Enum


class PaymentStatus(Enum):
    PENDING = "PENDING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"