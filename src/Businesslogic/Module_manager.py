from src.Data import Module_registrar
from src.Businesslogic.Registry import runtime_memory
import sys
import subprocess


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


    def run_module(self, module_name):
        module_paths = self.get_modules.get_custom_module_paths_from_registry()

        for module_path in module_paths:
            if module_path.name == module_name:

                self.process = subprocess.Popen([sys.executable, str(module_path)])

                try:
                    returncode = self.process.wait()
                finally:
                    self.process = None

                return

        print(f"Module not found: {module_name}")