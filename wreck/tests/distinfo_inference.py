import tempfile
import unittest
from pathlib import Path

from ..distinfo_inference import analyze


class DistinfoAnalyzeTest(unittest.TestCase):
    def test_analyze_simple(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "RECORD").write_text("foo/__init__.py,\n")

            dist = analyze(p)
            self.assertEqual({"foo"}, dist.provided_names)
            self.assertEqual(set(), dist.namespace_names)
            self.assertEqual({"foo"}, dist.minimal_names)

    def test_analyze_implicit_namespace(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "RECORD").write_text(
                """\
foo/bar/baz.py,
foo/bar/luhr.py,
foo/bar/text.txt,
../../usr/local/bin/foo,
"""
            )

            dist = analyze(p)
            self.assertEqual({"foo.bar.baz", "foo.bar.luhr"}, dist.provided_names)
            self.assertEqual({"foo", "foo.bar"}, dist.namespace_names)
            self.assertEqual({"foo.bar.baz", "foo.bar.luhr"}, dist.minimal_names)

    def test_analyze_namespace(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "RECORD").write_text(
                """\
foo/bar/__init__.py,
foo/bar/baz.py,
foo/bar/luhr.py,
"""
            )
            (p / "namespace_packages.txt").write_text("foo.bar\n\n")

            dist = analyze(p)
            self.assertEqual({"foo.bar.baz", "foo.bar.luhr"}, dist.provided_names)
            self.assertEqual({"foo", "foo.bar"}, dist.namespace_names)
            self.assertEqual({"foo.bar.baz", "foo.bar.luhr"}, dist.minimal_names)
