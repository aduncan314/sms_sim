"""
Module containing objects shared across multiple other modules.

Primarily, this module should contain only classes and datastructures used to
communicate between other modules.
"""

import datetime as dt
import typing as t
from dataclasses import dataclass
from enum import Enum

__all__ = ("SMSMessage", "SendResponse", "RuntimeEnv", "SingleSenderConfig", "ConfiguredSettings")


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
    AWS = "aws"


@dataclass(eq=True, frozen=True)
class SingleSenderConfig:
    name: str

    # Data
    mean_wait_ms: int
    std_wait_ms: int
    fail_rate: float

    @property
    def data(self) -> dict:
        return {name: val for name, val in vars().items() if name != "name"}


@dataclass(eq=True, frozen=True)
class ConfiguredSettings:
    runtime_env: RuntimeEnv
    senders: t.List[SingleSenderConfig]
    message_count: int
    monitor_period: int
