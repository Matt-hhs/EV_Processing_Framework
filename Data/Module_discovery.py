import yaml


def get_custom_modules_path():
    with open("config.yaml", "r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    if "custom_module_path" in data:
        return data["custom_module_path"]
    else:
        return None