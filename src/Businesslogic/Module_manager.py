from src.Data import Module_registrar
from src.Businesslogic.Registry import runtime_memory
from src.Data.Workflow_data_handler import data_handler, step_manager

import sys
import subprocess
import threading
import psutil


class GetFromRegistry:
    def __init__(self):
        self.registrar = Module_registrar.PutListInRegistry()


    def get_custom_module_names_from_registry(self):
        self.registrar.add_module_names_to_registry()
        
        return runtime_memory.get_entry_from_registry("custom_module_names")


    def get_custom_module_paths_from_registry(self):
        self.registrar.add_module_paths_to_registry()

        return runtime_memory.get_entry_from_registry("custom_modules")


class RunCustomModule:
    def __init__(self):
        self.get_modules = GetFromRegistry()
        self.process = None
        self.thread = None


    def is_alive(self):
        return self.thread is not None and self.thread.is_alive()


    def start(self, module_name):
        if self.is_alive():
            print("A module is already running.")
            return

        self.thread = threading.Thread(
            target=self.run_module,
            args=(module_name,),
            daemon=True
        )
        self.thread.start()


    def run_module(self, module_name):
        module_paths = self.get_modules.get_custom_module_paths_from_registry()

        for module_path in module_paths:
            if module_path.name == module_name:
                step_manager.set_step_module(module_path.name)
                step_manager.set_step_status("Processing")

                self.process = subprocess.Popen([sys.executable, str(module_path)])

                try:
                    returncode = self.process.wait()
                finally:
                    self.process = None

                if returncode == 0:
                    step_manager.set_step_status("Success")
                else:
                    step_manager.set_step_status("Failed")

                return

        print(f"Module not found: {module_name}")


    def pause(self):
        if not self.module_is_running():
            print("No module is running.")
            return

        psutil.Process(self.process.pid).suspend()
        print("Paused.")


    def resume(self):
        if not self.module_is_running():
            print("No module is running.")
            return

        psutil.Process(self.process.pid).resume()
        print("Resumed.")


    def stop(self):
        if not self.module_is_running():
            print("No module is running.")
            return

        process = psutil.Process(self.process.pid)

        process.resume()
        process.terminate()


    def module_is_running(self):
        return self.process is not None and self.process.poll() is None