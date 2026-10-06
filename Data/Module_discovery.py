import yaml
from pathlib import Path


class CustomModuleFinder:
    def get_data_from_yaml(self, variable_name: str):
        with open("config.yaml", "r", encoding="utf-8") as file:
            data = yaml.safe_load(file) or {}

        return data.get(variable_name)


    def ask_custom_modules_path(self):
        print()


    def check_folder_path(self):
        path = self.get_data_from_yaml("custom_module_path")

        if not path:
            path = self.ask_custom_modules_path()

        filepath = Path(path).expanduser()
        base = filepath.parent if filepath.name.lower() == "custom_modules" else filepath
        base = base.resolve()

        if not base.is_dir():
            raise FileNotFoundError(f"Location does not exist: {base}")
        
        folder = base / "custom_modules"

        if not folder.is_dir():
            raise FileNotFoundError(f"No 'custom_modules' folder in: {base}")

        return folder


    def find_custom_modules(self):
        allowed_suffixes = self.get_data_from_yaml("custom_module_suffixes")

        if not allowed_suffixes:
            print()

        found = []
        path = self.check_folder_path()

        for file in path.rglob("*"):
            if not file.is_file():
                continue

            if file.suffix.lower() not in allowed_suffixes:
                continue

            found.append(file)

        return sorted(found)