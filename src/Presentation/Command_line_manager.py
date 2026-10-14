from src.Businesslogic import Module_manager
from src.Businesslogic import Workflow_manager
import cmd
import threading
import psutil
import sys
import subprocess


class RunCustomModule:
    def __init__(self):
        self.get_modules = Module_manager.GetFromRegistry()
        self.run_modules = Module_manager.RunCustomModule()
        self.process = None
        self.thread = None


    def is_alive(self):
        return self.thread is not None and self.thread.is_alive()


    def start(self, module_name):
        if self.is_alive():
            print("A module is already running.")
            return

        self.thread = threading.Thread(
            target=self.run_modules.run_module,
            args=(module_name,),
            daemon=True
        )
        self.thread.start()


    def pause(self):
        if not self._module_is_running():
            print("No module is running.")
            return

        psutil.Process(self.process.pid).suspend()
        print("Paused.")


    def resume(self):
        if not self._module_is_running():
            print("No module is running.")
            return

        psutil.Process(self.process.pid).resume()
        print("Resumed.")


    def stop(self):
        if not self._module_is_running():
            print("No module is running.")
            return

        process = psutil.Process(self.process.pid)

        process.resume()
        process.terminate()


    def _module_is_running(self):
        return self.process is not None and self.process.poll() is None


class ProcessStatusManager(cmd.Cmd):
    intro = "Running EV_Processing_Framework. For available commands, type help."
    prompt = "> "

    def __init__(self):
        super().__init__()
        self.get_from_registry = Module_manager.GetFromRegistry()
        self.run_custom_module = RunCustomModule()
        self.manage_workflow = Workflow_manager.ManageWorkflow()


    def do_pause(self, arg):
        "Pause the current process."
        self.run_custom_module.pause()

    
    def do_resume(self, arg):
        "Resume a paused process."
        self.run_custom_module.resume()


    def do_stop(self, arg):
        "Stop the running process."
        self.run_custom_module.stop()


    def do_exit(self, arg):
        "Stop the running process and exit framework."
        if self.run_custom_module.is_alive():
            self.run_custom_module.stop()
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


    def do_run_module(self, arg):
        """Run a custom module located in the custom_modules folder by typing: run_module <module_name>"""
        module_name = arg.strip()

        if not module_name:
            return

        self.run_custom_module.start(
            module_name
        )


    def do_create_workflow(self, arg):
        """Create a new workflow with custom name by typing: create_workflow <workflow_name>"""
        workflow_name = arg.strip()

        if not workflow_name:
            return

        self.manage_workflow.create_workflow(workflow_name)

    def do_select_workflow(self, arg):
        """Select a the workflow you want to work in by typing: select_workflow <workflow_name>"""
        workflow_name = arg.strip()

        if not workflow_name:
            return

        self.manage_workflow.select_workflow(workflow_name)


def main():
    ProcessStatusManager().cmdloop()

if __name__ == "__main__":
    main()