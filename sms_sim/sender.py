import datetime as dt
import random
from time import sleep

from sms_sim.common import SMSMessage, SendResponse


class RandomSendError(RuntimeError):
    def __init__(self, *args):
        super().__init__("Send forced to fail.", *args)


class MessageSender:
    def __init__(self, mean_wait_ms: int, std_wait_ms: int = 1, fail_rate: float = 0.0):
        self._mean_wait_ms = float(mean_wait_ms)
        self._std_wait_ms = float(std_wait_ms)
        self._fail_rate = fail_rate

    def send_messages(self, message: SMSMessage) -> SendResponse:
        """
        Simulate sending a `message` with random send time and chance of failure.
        The send time is approximately normally distributed, based on the
        `mean_wait_ms` and `std_wait_ms` and failure rate is determined by
        `fail_rate`.

        Args:
            message: `SMSMessage` instance to "send"
        """
        start_time = dt.datetime.now()

        self._sleep()

        # TODO: Fail before or after sleep?
        if self._fail():
            return SendResponse(message, start_time, dt.datetime.now(), error=RandomSendError)
        try:
            return SendResponse(message, start_time, dt.datetime.now(), error=None)
        except Exception as e:
            return SendResponse(message, start_time, dt.datetime.now(), error=e)

    def _fail(self) -> bool:
        val = random.choices(population=(True, False), weights=(self._fail_rate, 1 - self._fail_rate))
        return val[0]

    def _sleep(self):
        # TODO: Confirm that truncating will not cause analysis errors
        wait_time_ms = random.normalvariate(self._mean_wait_ms, self._std_wait_ms)
        wait_time_ms = wait_time_ms if wait_time_ms > 0 else 0
        sleep(wait_time_ms / 1_000_000)
