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


    def start(self, module_name, parameters=None):
        if self.is_alive():
            print("A module is already running.")
            return

        self.thread = threading.Thread(
            target=self.run_module,
            args=(module_name, parameters or {}),
            daemon=True
        )
        self.thread.start()


    def run_module(self, module_name, parameters):
        module_paths = self.get_modules.get_custom_module_paths_from_registry()

        for module_path in module_paths:
            if module_path.name == module_name:
                arguments = self.check_module_input(module_path, parameters)

                if arguments is None or not self.check_input_type(module_path):
                    return

                step_manager.set_step_module(module_path.name)
                step_manager.set_step_output_type(self.get_module_config(module_path, "output_type"))
                step_manager.set_step_status("Processing")

                self.process = subprocess.Popen([sys.executable, str(module_path)] + arguments)


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


    def convert_parameter(self, value, parameter_type):
        if parameter_type == "int":
            return int(value)
        
        if parameter_type == "float":
            return float(value)
        
        if parameter_type == "bool":
            if str(value).lower() in ("true", "1", "yes"):
                return True
            
            if str(value).lower() in ("false", "0", "no"):
                return False
            
            raise ValueError(value)

        return str(value)


    def get_module_config(self, module_path, key):
        return self.get_modules.registrar.module_discovery.get_module_config(module_path, key)


    def check_input_type(self, module_path):
        input_types = self.get_module_config(module_path, "input_types")

        if not input_types:
            return True

        parent_output_type = step_manager.get_parent_output_type()

        if parent_output_type is None:
            return True

        if parent_output_type not in input_types:
            print(f"Module accepts {input_types}, but the previous step outputs '{parent_output_type}'.")
            return False

        return True


    def check_module_input(self, module_path, parameters):
        """Validates parameters against the module's yaml and returns a list of command line arguments, or None if invalid."""
        specification = self.get_module_config(module_path, "parameters") or {}
        arguments = []
        valid = True

        for name in parameters:
            if name not in specification:
                print(f"Unknown parameter: {name}")
                valid = False

        for name, rules in specification.items():
            rules = rules or {}

            if name not in parameters:
                if rules.get("required", False):
                    print(f"Missing required parameter: {name}")
                    valid = False
                continue

            parameter_type = rules.get("type", "str")

            try:
                value = self.convert_parameter(parameters[name], parameter_type)
            except ValueError:
                print(f"Parameter '{name}' must be of type {parameter_type}.")
                valid = False
                continue

            allowed = rules.get("allowed")
            minimum = rules.get("min")
            maximum = rules.get("max")

            if allowed is not None and value not in allowed:
                print(f"Parameter '{name}' must be one of: {allowed}")
                valid = False

            elif minimum is not None and value < minimum:
                print(f"Parameter '{name}' must be >= {minimum} and <= {maximum}.")
                valid = False

            elif maximum is not None and value > maximum:
                print(f"Parameter '{name}' must be >= {minimum} and <= {maximum}.")
                valid = False
            else:
                arguments += [f"--{name}", str(value)]

        if not valid:
            return None

        return arguments


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