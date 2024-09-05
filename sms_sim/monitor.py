from __future__ import annotations

import time
import typing as t
from enum import Enum
from functools import reduce
from multiprocessing import Queue

from sms_sim.common import SendResponse


class MonitorSource(Enum):
    AWS = "aws"
    MULTIPROC = "multi_proc"
    SINGLEPROC = "single_proc"


class Monitor:
    def __init__(
        self,
        update_period: int,
        source: MonitorSource = MonitorSource.MULTIPROC,
        queue: t.Optional[Queue[SendResponse] | t.Iterable[SendResponse]] = None,
    ):
        self._update_period = update_period
        self._queue = queue

        if source == MonitorSource.MULTIPROC:
            # TODO: This doesn't work and fixing breaks the mp context
            # assert isinstance(self._queue, Queue)
            self.get_next = self._multi_proc_get_next
        elif source == MonitorSource.SINGLEPROC:
            self.get_next = self._single_proc_get_next
        elif source == MonitorSource.AWS:
            self.get_next = self._aws_get_next
        else:
            raise ValueError(f"Expected {MonitorSource} but found {source}")

    def start(self):
        print(f"Queue in monitor : {self._queue.qsize()}")
        buffer = []
        start_time = time.time()
        while True:
            try:
                _next = self.get_next()
                buffer.append(_next)
            except Exception as e:
                pass
            thingy = time.time() - start_time
            if thingy > self._update_period:
                start_time = time.time()
                self._publish(buffer)

    def _publish(self, buffer: t.List[SendResponse]):
        message_count = len(buffer)
        failed_count = len([r for r in buffer if not r.success])
        total_msg_time = reduce(lambda x, y: x + y, [r.end_time - r.start_time for r in buffer])
        mean_msg_time = total_msg_time.total_seconds() / message_count

        print(
            f"UPDATE:\n"
            f"messages sent:\t{message_count}\n"
            f"messages failed:\t{failed_count}\n"
            f"mean send time:\t{mean_msg_time}\n\n"
        )

    def _multi_proc_get_next(self) -> SendResponse:
        # _get = partial(self._queue.get, timeout=10)
        # for i in iter(_get, "STOP"):
        #     yield i
        return self._queue.get(timeout=0.5)

    def _single_proc_get_next(self) -> SendResponse:
        # TODO: Is this even an option?
        raise NotImplementedError(f'"_single_proc_get_next" method is not currently supported.')

    def _aws_get_next(self) -> SendResponse:
        raise NotImplementedError(f'"_aws_get_next" method is not currently supported.')
