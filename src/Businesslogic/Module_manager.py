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


    def run_module(self, custom_module_name):
        module_paths = self.get_modules.get_custom_module_paths_from_registry()

        for module in module_paths:
            if module.endswith(custom_module_name):
                subprocess.run(
                    [sys.executable, module]
                )