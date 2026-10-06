import yaml
from pathlib import Path


def get_custom_modules_path():
    with open("config.yaml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    if "custom_module_path" in data:
        return data["custom_module_path"]
    else:
        return None


def ask_custom_modules_path():
    print()


def check_folder_path():
    path = get_custom_modules_path()

    if not path:
        path = ask_custom_modules_path()

    filepath = Path(path).expanduser()
    base = filepath.parent if filepath.name.lower() == "custom_modules" else filepath
    base = base.resolve()

    if not base.is_dir():
        raise FileNotFoundError(f"Location does not exist: {base}")
    
    folder = base / "custom_modules"

    if not folder.is_dir():
        raise FileNotFoundError(f"No 'custom_modules' folder in: {base}")


    


    

