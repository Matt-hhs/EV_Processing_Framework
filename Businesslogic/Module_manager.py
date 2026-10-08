from Data import Module_registrar
from Businesslogic.Registry import runtime_memory


class GetFromRegistry:
    def __init__(self):
        self.registrar = Module_registrar.PutListInRegistry()


    def get_custom_module_names_from_registry(self):
        self.registrar.add_module_names_to_registry()
        
        return runtime_memory.get_entry_from_registry("custom_module_names")
