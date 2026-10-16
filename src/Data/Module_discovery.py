import yaml
from pathlib import Path


class CustomModuleFinder:
    def get_data_from_yaml(self, yaml_path: str, variable_name: str):
        with open(yaml_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}

        return data.get(variable_name)


    def get_module_config(self, module_path, variable):
        yaml_path = Path(module_path).with_suffix(".yaml")

        if not yaml_path.is_file():
            return None

        return self.get_data_from_yaml(str(yaml_path), variable)


    def ask_custom_modules_path(self):
        # TODO
        print()


    def check_folder_path(self):
        path = self.get_data_from_yaml("config.yaml", "custom_module_path")

        if not path:
            path = self.ask_custom_modules_path()

        if not path:
            raise ValueError("No custom module path was provided! Add \'custom_module_path: <path>\' to config.yaml")

        filepath = Path(path).expanduser()

        if filepath.name.lower() == "custom_modules":
            base = filepath.parent
        else:
            base = filepath

        base = base.resolve()

        if not base.is_dir():
            raise FileNotFoundError(f"Location does not exist: {base}")
        
        folder = base / "custom_modules"

        if not folder.is_dir():
            raise FileNotFoundError(f"No 'custom_modules' folder in: {base}")

        return folder


    def find_custom_modules(self):
        allowed_suffixes = self.get_data_from_yaml("config.yaml", "custom_module_suffixes")

        if not allowed_suffixes:
            raise ValueError("No prefixes were provided! Add the following to config.yaml:\n\'allowed_suffixes:\n  - \"<suffix>\"\'")

        found = []
        path = self.check_folder_path()

        for file in path.rglob("*"):
            if not file.is_file():
                continue

            if file.suffix.lower() not in allowed_suffixes:
                continue

            found.append(file)

        return sorted(found)