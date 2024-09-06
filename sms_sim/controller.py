# For testing/local
from multiprocessing import Process, Queue
from queue import Empty

from sms_sim.common import ConfiguredSettings, RuntimeEnv
from sms_sim.monitor import start
from sms_sim.producer import create_phone_messages
from sms_sim.sender import MessageSender

TIMEOUT = 5


class LocalController:
    """
    Class that runs all portions of the code when running on a single machine.

    Creates messages to send and "sends" the messages with the `MessageSender`
    objects determined by `settings`.

    Each `MessageSender` runs in its own process. Messages are distributed
    first come which may cause some `MessageSender` instances to "send" more.
    There is no limit to the number of `MessageSenders`, however, there will be
    diminished returns if the number of processes exceeds CPU cores.

    Args:
        settings: A `ConfiguredSettings` instance with all current settings
        timeout: Timeout for multiprocessing queue put/get in seconds (default: 5 seconds)
    """

    def __init__(self, settings: ConfiguredSettings, timeout: int = TIMEOUT):
        super().__init__()
        self._config = settings
        self._timeout = timeout
        self._senders = []
        self._msg_count = 0

        self._msg_queue = Queue()
        self._out_queue = Queue()

        self._create_senders()

    def submit_messages(self):
        """Create messages and add them to the message queue."""
        for msg in create_phone_messages(self._config.message_count):
            self._msg_queue.put(msg, timeout=self._timeout)
            self._msg_count += 1

    def _create_senders(self):
        for sender in self._config.senders:
            self._senders.append(MessageSender(sender.mean_wait_ms, sender.std_wait_ms, sender.fail_rate))

    def run(self):
        """Run the main program loop. See class docstring for more details."""
        print(
            f"Running SMS simulation with {len(self._senders)} simulated sender{'s' if len(self._senders) > 1 else ''}."
        )
        procs = []

        for sender in self._senders:
            p = Process(target=message_worker, args=(sender, self._msg_queue, self._out_queue, self._timeout))
            procs.append(p)

        # Create separate process for monitor
        monitor_p = Process(
            target=monitor_worker, args=(self._out_queue, self._config.monitor_period, self._config.runtime_env)
        )
        procs.append(monitor_p)

        for p in procs:
            p.start()

        for p in procs:
            p.join()


def message_worker(sender: MessageSender, in_q: Queue, out_q: Queue, timeout: int):
    try:
        while True:
            msg = in_q.get(timeout=timeout)
            if msg:
                response = sender.send_messages(msg)
                out_q.put(response, timeout=timeout)
    except Empty:
        return


def monitor_worker(out_q: Queue, period: int, env: RuntimeEnv):
    start(queue=out_q, update_period=period, env=env)
