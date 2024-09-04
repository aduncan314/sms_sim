from sms_sim import producer


def test_producer_basic():
    msg = list(producer.create_phone_messages(10))
    assert len(msg) == 10


def test_phone_number_format():
    rand_num = producer._gen_random_number()
    # USA number skipping country code with "-" separator
    assert len(rand_num) == 12
    assert rand_num[3] == rand_num[7] == "-"


def test_message():
    rand_msg = producer._gen_random_message(10)
    assert len(rand_msg) == 10
