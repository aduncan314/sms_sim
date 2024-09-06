from sms_sim import common
from sms_sim import sender


def test_sender_fail():
    test_message_sender = sender.MessageSender(0, 0, 1)
    test_message = common.SMSMessage("555-555-5555", "HEY")
    send_response = test_message_sender.send_messages(test_message)

    assert send_response.error is sender.RandomSendError


def test_sender_success():
    test_message_sender = sender.MessageSender(0, 0, 0)
    test_message = common.SMSMessage("555-555-5555", "HEY")

    send_response = test_message_sender.send_messages(test_message)

    assert send_response.error is None

def test_sender_wait():
    test_message_sender = sender.MessageSender(0, 0, 0)
    test_message = common.SMSMessage("555-555-5555", "HEY")
    send_response = test_message_sender.send_messages(test_message)

    assert (send_response.end_time - send_response.start_time).total_seconds() < 0.00005

    test_message_sender = sender.MessageSender(1000, 0, 0)
    test_message = common.SMSMessage("555-555-5555", "HEY")
    send_response = test_message_sender.send_messages(test_message)

    assert 0.0008 < (send_response.end_time - send_response.start_time).total_seconds() < .0012
