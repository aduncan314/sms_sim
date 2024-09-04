import random
import typing as t
from functools import partial

from sms_sim.common import SMSMessage


def _create_random_message(
    num_func: t.Callable[[], str], msg_func: t.Callable[[], str]
) -> SMSMessage:
    num = num_func()
    msg = msg_func()
    return SMSMessage(phone_number=num, message=msg)


def _gen_random_number() -> str:
    return f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"


def _gen_random_message(msg_len: int = 100) -> str:
    population = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    return "".join(random.choices(population, k=msg_len))


# TODO: Add backoff here or elsewhere?
def create_phone_messages(
    num: int,
    number_func: t.Callable = _gen_random_number,
    message_func: t.Callable = _gen_random_message,
) -> t.Generator[SMSMessage, None, None]:
    bound_message_creator = partial(_create_random_message, number_func, message_func)
    return (bound_message_creator() for i in range(num))
