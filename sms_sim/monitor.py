from __future__ import annotations

import time
import typing as t
from functools import reduce
from multiprocessing import Queue
from queue import Empty

from sms_sim.common import SendResponse, RuntimeEnv


def _choose_func(source: RuntimeEnv) -> t.Callable[[t.Any], SendResponse]:
    if source == RuntimeEnv.LOCAL:
        return _multi_proc_get_next
    elif source == RuntimeEnv.AWS:
        return _aws_get_next
    else:
        raise ValueError(f"Expected {RuntimeEnv} but found {source}.")


def start(update_period: int, env: RuntimeEnv, queue: Queue):
    get_next = _choose_func(env)

    buffer = []
    start_time = time.time()
    while True:
        try:
            _next = get_next(queue)
            buffer.append(_next)
        except Empty:
            # Q may be empty due to latency or all messages being sent
            pass
        time_since_last_update = time.time() - start_time
        if time_since_last_update > update_period:
            start_time = time.time()
            _publish(buffer)


def _publish(buffer: t.List[SendResponse]):
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


def _multi_proc_get_next(queue) -> SendResponse:
    return queue.get(timeout=0.5)


def _aws_get_next(queue) -> SendResponse:
    raise NotImplementedError(f'"_aws_get_next" method is not currently supported.')
