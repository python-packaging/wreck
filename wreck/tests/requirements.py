import tempfile
import unittest
from pathlib import Path

from ..requirements import iter_glob_all_requirement_names, iter_requirement_names


class RequirementsTest(unittest.TestCase):
    def test_iter_requirement_names(self) -> None:
        with tempfile.NamedTemporaryFile() as f:
            f.write(b"foo\n\nBar==1.0\r\nbaz ; python_version < '3.7'\n")
            f.flush()
            names = list(iter_requirement_names(Path(f.name)))
            self.assertEqual(["foo", "bar", "baz"], names)

    def test_glob_all_requirement_names(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "requirements.txt").write_text("foo")
            (p / "requirements-dev.txt").write_text("bar\nbaz")

            # we sort the glob output for consistency, but this puts the
            # requirements-dev first :/
            names = list(
                iter_glob_all_requirement_names(f"{p.as_posix()}/requirements*.txt")
            )
            self.assertEqual(["bar", "baz", "foo"], names)

            names = list(
                iter_glob_all_requirement_names(f"{p.as_posix()}/requirements*.txt,")
            )
            self.assertEqual(["bar", "baz", "foo"], names)
