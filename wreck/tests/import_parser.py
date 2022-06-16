import tempfile
import unittest
from pathlib import Path

from ..import_parser import get_imports


class ImportParserTest(unittest.TestCase):
    def test_import(self) -> None:
        with tempfile.NamedTemporaryFile() as f:
            f.write(b"import a\nimport a.b\n")
            f.flush()

            imports = get_imports(Path(f.name))
            self.assertEqual({"a", "a.b"}, imports)

    def test_fromimport(self) -> None:
        with tempfile.NamedTemporaryFile() as f:
            f.write(b"from a import b\nfrom x import y, z as zzz\n")
            f.flush()

            imports = get_imports(Path(f.name))
            self.assertEqual({"a.b", "x.y", "x.z"}, imports)
