from Businesslogic import Module_manager
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


    def pause(self):
        self._running.clear()
        print("Paused.")


    def resume(self):
        self._running.set()
        print("Resumed.")


    def stop(self):
        self._stop.set()
        self._running.set()

        if self._thread:
            # Block thread until self._thread has stopped
            self._thread.join()
        print("Stopped.")


class ProcessStatusManager(cmd.Cmd):
    intro = "Running EV_Processing_Framework. For available commands, type help."
    prompt = "> "

    def __init__(self):
        super().__init__()
        self.runner = ProcessRunner()
        self.get_from_registry = Module_manager.GetFromRegistry()


    def do_start(self, arg):
        "Start the process."
        self.runner.start


    def do_pause(self, arg):
        "Pause the current process."
        self.runner.pause()

    
    def do_resume(self, arg):
        "Resume a paused process."
        self.runner.resume()


    def do_stop(self, arg):
        "Stop the running process."
        self.runner.stop()


    def do_exit(self, arg):
        "Stop the running process and exit framework."
        if self.runner.is_alive():
            self.runner.stop()
        return True

    do_EOF = do_exit


    def do_get_custom_modules(self, arg):
        "Returns custom modules found in dedicated folder(s)."
        custom_modules = self.get_from_registry.get_custom_module_names_from_registry()

        if not custom_modules:
            print("No modules found!")
            return

        print("Custom modules: ")
        for module in custom_modules:
            print(f"- {module}")

    


def main():
    ProcessStatusManager().cmdloop()

if __name__ == "__main__":
    main()