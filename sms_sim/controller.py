# For testing/local
from multiprocessing import Process, Queue
from queue import Empty

from sms_sim.monitor import Monitor
from sms_sim.producer import create_phone_messages
from sms_sim.sender import MessageSender

TIMEOUT = 10


class ControllerBase:
    def __init__(self):
        pass

    def run(self):
        raise NotImplementedError()


# TODO: Does this even make sense?
class LambdaController(ControllerBase):
    def run(self):
        # Just run one?
        pass


class LocalSenderController(ControllerBase):
    def __init__(self, config: dict):
        super().__init__()
        self._sender_config = config["senders"]
        self._senders = {}
        self._msg_count = 0

        self._msg_queue = Queue()
        self._out_queue = Queue()

        self._create_senders()

    def submit_messages(self):
        for msg in create_phone_messages(10000):
            self._msg_queue.put(msg, timeout=TIMEOUT)  # TODO: Add timeout?
            self._msg_count += 1

    def _create_senders(self):
        for sender in self._sender_config:
            name = sender["name"]
            self._senders[name] = MessageSender(**sender["args"])

    def run(self):
        procs = []

        for name, sender in self._senders.items():
            print(f"Starting {name}...")
            p = Process(
                target=message_worker, args=(sender, self._msg_queue, self._out_queue)
            )
            procs.append(p)
        monitor_p = Process(target=monitor_worker, args=(self._out_queue,))
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
                # print(f"In controller, output q has {out_q.qsize()}")
    except Empty:
        print("empty")
        return


def monitor_worker(out_q: Queue):
    m = Monitor(update_period=5, queue=out_q)
    m.start()
