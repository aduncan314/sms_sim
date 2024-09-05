import datetime as dt
import random
from time import sleep

from sms_sim.common import SMSMessage, SendResponse


class MessageSender:
    def __init__(self, mean_wait_ms: int, std_wait_ms: int = 1, fail_rate: float = 0.0):
        self._mean_wait_ms = float(mean_wait_ms)
        self._std_wait_ms = float(std_wait_ms)
        self._fail_rate = fail_rate

    def send_messages(self, message: SMSMessage) -> SendResponse:
        start_time = dt.datetime.now()
        if self._fail():
            # print(f"Message to {message.phone_number} set to fail.")
            return SendResponse(message, False, "Random", start_time, dt.datetime.now())

        wait_time_ms = abs(random.normalvariate(self._mean_wait_ms, self._std_wait_ms))  # TODO: this is wrong
        # print(f"Sending message to {message.phone_number} with wait time {wait_time_ms}")
        sleep(wait_time_ms / 1_000_000)
        try:
            return self._send(message, start_time)
        except Exception as e:
            # TODO: Perhaps just raise, perhaps include exception in response obj
            return SendResponse(message, False, str(e), start_time, dt.datetime.now())

    def _fail(self) -> bool:
        val = random.choices(population=(True, False), weights=(self._fail_rate, 1 - self._fail_rate))
        return val[0]

    @staticmethod
    def _send(message: SMSMessage, start_time: dt.datetime) -> SendResponse:
        # print(f"Sending SMS message to {message.phone_number}:\n{message.message}\\n")
        return SendResponse(message, True, "", start_time, dt.datetime.now())

    def _log(self, message: SMSMessage):
        pass
