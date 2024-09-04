import datetime as dt
from dataclasses import dataclass
from enum import Enum

__all__ = ("SMSMessage", "SendResponse", "RuntimeEnv")


@dataclass
class SMSMessage:
    phone_number: str
    message: str


@dataclass
class SendResponse:
    message: SMSMessage
    success: bool
    reason: str
    start_time: dt.datetime
    end_time: dt.datetime


class RuntimeEnv(str, Enum):
    LOCAL = "local"
    LOCAL_NETWORK = "local_network"
    AWS = "aws"
