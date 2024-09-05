# For testing/local
from multiprocessing import Process, Queue
from queue import Empty

from sms_sim.monitor import Monitor
from sms_sim.producer import create_phone_messages
from sms_sim.sender import MessageSender
from sms_sim.common import ConfiguredSettings

TIMEOUT = 10


class LocalSenderController:
    def __init__(self, settings: ConfiguredSettings):
        super().__init__()
        self._config = settings
        self._senders = {}
        self._msg_count = 0

        self._msg_queue = Queue()
        self._out_queue = Queue()

        self._create_senders()

    def submit_messages(self):
        for msg in create_phone_messages(self._config.message_count):
            self._msg_queue.put(msg, timeout=TIMEOUT)
            self._msg_count += 1

    def _create_senders(self):
        for sender in self._config.senders:
            self._senders[sender.name] = MessageSender(sender.mean_wait_ms, sender.std_wait_ms, sender.fail_rate)

    def run(self):
        procs = []

        for name, sender in self._senders.items():
            print(f"Starting {name}...")
            p = Process(target=message_worker, args=(sender, self._msg_queue, self._out_queue))
            procs.append(p)
        monitor_p = Process(target=monitor_worker, args=(self._out_queue, self._config.monitor_period))
        procs.append(monitor_p)

        for p in procs:
            p.start()

        for p in procs:
            p.join()

        print("Exiting.")


def message_worker(sender: MessageSender, in_q: Queue, out_q: Queue):
    print(f"In worker for {sender}")
    print(f"In queue: {in_q}: {in_q.qsize()}")
    try:
        while True:
            msg = in_q.get(timeout=TIMEOUT)
            if msg:
                response = sender.send_messages(msg)
                out_q.put(response, timeout=TIMEOUT)
    except Empty:
        return


def monitor_worker(out_q: Queue, period: int):
    m = Monitor(update_period=period, queue=out_q)
    m.start()
