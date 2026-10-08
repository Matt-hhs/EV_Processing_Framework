from typing import Any

class RuntimeMemory:
    def __init__(self):
        self.registry: dict[str, Any] = {
            "custom_modules": [],
            "custom_module_names": []
        }


    def get_entry_from_registry(self, registry_name: str):
        if registry_name in self.registry:
            return self.registry.get(registry_name)


    def add_entry_to_registry(self, item: str, registry_name: str):
        wanted_registry = self.registry.get(registry_name)

        if wanted_registry is None:
            print("Registry not found")

        elif isinstance(wanted_registry, list):
            wanted_registry.append(item)


    def clear_registry(self, registry_name: str):
        registry = self.registry.get(registry_name)

        if registry is None:
            print("Registry not found")
            return

        registry.clear()


runtime_memory = RuntimeMemory()