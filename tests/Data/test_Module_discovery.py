import unittest
import tempfile
import os
import re
import yaml
from pathlib import Path
from unittest.mock import patch

from src.Data.Module_discovery import CustomModuleFinder


class TestGetDataFromYaml(unittest.TestCase):
    def make_config(self, yaml_text):
        fp = tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8")

        self.addCleanup(os.remove, fp.name)
        fp.write(yaml_text)
        fp.close()
        return fp.name


    def test_reads_string(self):
        yaml_path = self.make_config("testkey: testing123")

        result = CustomModuleFinder().get_data_from_yaml(yaml_path, "testkey")

        self.assertEqual(result, "testing123")


    def test_read_list(self):
        yaml_path = self.make_config("multiple_items:\n  - \"item1\"\n  - \"item2\"")

        result = CustomModuleFinder().get_data_from_yaml(yaml_path, "multiple_items")

        self.assertEqual(result, ["item1", "item2"])


    def test_return_none_for_empty_yaml(self):
        yaml_path = self.make_config("")

        result = CustomModuleFinder().get_data_from_yaml(yaml_path, "missing_key")

        self.assertIsNone(result)


    def test_nested_data(self):
        yaml_path = self.make_config("nest1:\n  nest1.1: true\n  nest2:\n    nest3: 45")

        result = CustomModuleFinder().get_data_from_yaml(yaml_path, "nest1")

        self.assertEqual(result, {"nest1.1": True, "nest2":  {"nest3": 45}})


    def test_return_none_for_no_key(self):
        yaml_path = self.make_config("xy: 25\nx: 5")

        result = CustomModuleFinder().get_data_from_yaml(yaml_path, "y")

        self.assertIsNone(result)


    def test_get_null_value(self):
        yaml_path = self.make_config("xy: null")
        
        result = CustomModuleFinder().get_data_from_yaml(yaml_path, "xy")

        self.assertIsNone(result)


    def test_missing_file_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            CustomModuleFinder().get_data_from_yaml("does_not_exist.yaml", "key")


    def test_invalid_yaml_raises_error(self):
        yaml_path = self.make_config("key: [unclosed")

        with self.assertRaises(yaml.YAMLError):
            CustomModuleFinder().get_data_from_yaml(yaml_path, "key")


class TestGetModuleConfig(unittest.TestCase):
    def make_config(self, yaml_text):
        fp = tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8")

        self.addCleanup(os.remove, fp.name)
        fp.write(yaml_text)
        fp.close()
        return fp.name


    def test_returns_value_from_yaml(self):
        yaml_path = self.make_config("number: 1")
        module_path = os.path.splitext(yaml_path)[0] + ".py"

        result = CustomModuleFinder().get_module_config(module_path, "number")

        self.assertEqual(result, 1)


    def test_returns_none_when_yaml_is_missing(self):
        module_path = "/tmp/random_script.py"

        result = CustomModuleFinder().get_module_config(module_path, "number")

        self.assertIsNone(result)


    def test_returns_none_when_variable_is_missing(self):
        yaml_path = self.make_config("decimal: 1")
        module_path = os.path.splitext(yaml_path)[0] + ".py"

        result = CustomModuleFinder().get_module_config(module_path, "number")

        self.assertIsNone(result)


    def test_returns_none_when_yaml_is_empty(self):
        yaml_path = self.make_config("")
        module_path = os.path.splitext(yaml_path)[0] + ".py"

        result = CustomModuleFinder().get_module_config(module_path, "number")

        self.assertIsNone(result)


class TestCheckFolderPath(unittest.TestCase):
    def setUp(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        self.base = Path(temp_dir.name).resolve()

        previous_directory = os.getcwd()
        os.chdir(self.base)
        self.addCleanup(os.chdir, previous_directory)


    def write_config(self, path=None):
        if path is None:
            text = ""
        else:
            text = f'custom_module_path: "{path}"\n'

        base = self.base / "config.yaml"
        
        base.write_text(text, encoding="utf-8")


    def test_returns_custom_modules_folder(self):
        folder = self.base / "custom_modules"
        folder.mkdir()
        self.write_config(self.base)

        result = CustomModuleFinder().check_folder_path()

        self.assertEqual(result, folder)
        self.assertTrue(result.is_dir())


    def test_path_pointing_to_custom_modules_uses_parent(self):
        folder = self.base / "custom_modules"
        folder.mkdir()
        self.write_config(folder)

        result = CustomModuleFinder().check_folder_path()

        self.assertEqual(result, folder)


    def test_custom_modules_name_is_case_insensitive(self):
        folder = self.base / "custom_modules"
        folder.mkdir()
        self.write_config(self.base / "Custom_Modules")

        result = CustomModuleFinder().check_folder_path()

        self.assertEqual(result, folder)


    def test_asks_for_path_when_not_in_config(self):
        folder = self.base / "custom_modules"
        folder.mkdir()
        self.write_config()
        finder = CustomModuleFinder()

        with patch.object(finder, "ask_custom_modules_path", return_value=str(self.base)) as ask:
            result = finder.check_folder_path()

        ask.assert_called_once()
        self.assertEqual(result, folder)


    def test_missing_base_directory_raises_error(self):
        folder = self.base / "does_not_exist"
        self.write_config(folder)

        with self.assertRaisesRegex(FileNotFoundError, "Location does not exist"):
            CustomModuleFinder().check_folder_path()


    def test_base_is_a_file_raises_error(self):
        file_path = self.base / "some_file.txt"
        file_path.write_text("x", encoding="utf-8")
        self.write_config(file_path)

        with self.assertRaisesRegex(FileNotFoundError, "Location does not exist"):
            CustomModuleFinder().check_folder_path()


    def test_missing_custom_modules_folder_raises_error(self):
        self.write_config(self.base)

        with self.assertRaisesRegex(FileNotFoundError, "No 'custom_modules' folder"):
            CustomModuleFinder().check_folder_path()


    def test_custom_modules_is_a_file_raises_error(self):
        custom_modules = self.base / "custom_modules"
        custom_modules.write_text("x", encoding="utf-8")
        self.write_config(self.base)

        with self.assertRaisesRegex(FileNotFoundError, "No 'custom_modules' folder"):
            CustomModuleFinder().check_folder_path()


    def test_raises_error_when_config_and_user_provide_no_path(self):
        self.write_config()
        finder = CustomModuleFinder()

        with patch.object(finder, "ask_custom_modules_path", return_value=None):
            with self.assertRaisesRegex(ValueError, "No custom module path was provided"):
                finder.check_folder_path()



if __name__ == '__main__':
    unittest.main()