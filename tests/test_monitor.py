import datetime as dt
from multiprocessing import Queue

import pytest

from sms_sim import common
from sms_sim import monitor


@pytest.mark.skip(reason="Not ready")
def test_basic_monitor(capsys):
    assert False
    # q = Queue()
    # q.put(
    #     common.SendResponse(
    #         message=common.SMSMessage("555-555-5555", "HEY"),
    #         success=True,
    #         reason="",
    #         start_time=dt.datetime.now() + dt.timedelta(seconds=-1),
    #         end_time=dt.datetime.now(),
    #     ),
    # )
    # m = monitor.Monitor(
    #     update_period=1, source=monitor.MonitorSource.MULTIPROC, queue=q
    # )
    # m.start()
    # captured = capsys.readouterr()
    # q.join_thread()
    # assert captured.out == ""
