import random
import string
import typing as t
from functools import partial

from sms_sim.common import SMSMessage


def _create_random_message(num_func: t.Callable[[], str], msg_func: t.Callable[[], str]) -> SMSMessage:
    return SMSMessage(phone_number=num_func(), message=msg_func())


def _gen_random_number() -> str:
    return f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"


def _gen_random_message(msg_len: int = 100) -> str:
    population = string.ascii_uppercase + " "
    return "".join(random.choices(population, k=msg_len))


# TODO: Add backoff here or elsewhere?
def create_phone_messages(
    num: int,
    number_func: t.Callable = _gen_random_number,
    message_func: t.Callable = _gen_random_message,
) -> t.Generator[SMSMessage, None, None]:
    """
    Generate `SMSMessage` objects using `number_func` and `message_func`. The
    number of messages is determined by `num`.

    Args:
        num: Number of messages
        number_func: Function with no args that returns a random phone number
        message_func: Function with no args that returns a random message
    """
    bound_message_creator = partial(_create_random_message, number_func, message_func)
    return (bound_message_creator() for i in range(num))
