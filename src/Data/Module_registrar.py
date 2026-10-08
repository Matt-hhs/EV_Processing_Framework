""" 
1. Get the custom_modules from module_discovery
2. Convert it (optional)
3. Insert it

4. Communicate with module_manager that the module_discovery needs a filepath from user
"""
from src.Data import Module_discovery
from src.Businesslogic.Registry import runtime_memory
from pathlib import Path


class PutListInRegistry:
    def __init__(self):
        self.module_discovery = Module_discovery.CustomModuleFinder()


    def get_module_paths_from_discovery(self):
        return self.module_discovery.find_custom_modules()


    def convert_module_filepaths_to_filename(self):
        module_paths = self.get_module_paths_from_discovery()
        module_names = []

        for module in module_paths:
            module_name = Path(module).name
            module_names.append(module_name)

        return module_names


    def add_module_names_to_registry(self):
        module_names = self.convert_module_filepaths_to_filename()

        runtime_memory.clear_registry("custom_module_names")

        for module_name in module_names:
            runtime_memory.add_entry_to_registry(module_name, "custom_module_names")


    def add_module_paths_to_registry(self):
        module_paths = self.get_module_paths_from_discovery()

        runtime_memory.clear_registry("custom_modules")

        for module_path in module_paths:
            runtime_memory.add_entry_to_registry(module_path, "custom_modules")