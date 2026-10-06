import cmd
import threading


class ProcessRunner:
    def __init__(self):
        self._thread = None

        # .set() = True | .wait() = block thread until True | .clear() = False
        self._stop = threading.Event()
        self._running = threading.Event()

    def is_alive(self):
        return self._thread is not None and self._thread.is_alive()

    def start(self):
        if self.is_alive():
            return
        self._stop.clear()
        self._running.set()
        self._thread = threading.Thread(target=self._work, daemon=True)
        self._thread.start()


class ProcessStatusManager(cmd.Cmd):
    intro = "Running EV_Processing_Framework. For available commands, type help."
    prompt = "> "

    def __init__(self):
        super().__init__()
        self.runner = ProcessRunner()

    def do_start(self, arg):
        "Start the process."
        self.runner.start


def main():
    ProcessStatusManager().cmdloop()

if __name__ == "__main__":
    main()