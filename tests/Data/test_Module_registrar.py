from src.Data.Module_registrar import PutListInRegistry

import unittest
from unittest.mock import Mock, patch
from pathlib import Path


class TestGetModulePathsFromDiscovery(unittest.TestCase):
    def test_returns_paths_from_module_discovery(self):
        expected_paths = [Path("/modules/first.py"), Path("/modules/second.py")]

        registrar = PutListInRegistry()
        registrar.module_discovery = Mock()
        registrar.module_discovery.find_custom_modules.return_value = expected_paths

        result = registrar.get_module_paths_from_discovery()

        registrar.module_discovery.find_custom_modules.assert_called_once_with()
        self.assertEqual(result, expected_paths)


class TestConvertModuleFilepathsToFilename(unittest.TestCase):
    def test_returns_module_names(self):
        expected_paths = [Path("/modules/first.py"), Path("/modules/second.py")]

        registrar = PutListInRegistry()

        with patch.object(registrar, "get_module_paths_from_discovery", return_value=expected_paths,):
            result = registrar.convert_module_filepaths_to_filename()

        self.assertEqual(result, ["first.py", "second.py"])

if __name__ == '__main__':
    unittest.main()