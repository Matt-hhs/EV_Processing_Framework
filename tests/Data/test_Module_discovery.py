import unittest
import tempfile
import os

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


if __name__ == '__main__':
    unittest.main()