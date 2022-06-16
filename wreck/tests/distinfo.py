import unittest

from ..distinfo import iter_all_distinfo_dirs


class DistinfoTest(unittest.TestCase):
    def test_iter_all_distinfo_dirs(self) -> None:
        # This is a very cursory test, that just ensures we can find one of the
        # distinfo dirs that ought to exist.
        for project, version, subdir in iter_all_distinfo_dirs():
            if project == "click":
                self.assertTrue(subdir.is_dir())
                self.assertTrue(subdir.name.endswith(".dist-info"))
                self.assertIsInstance(version, str)
                break
        else:
            self.fail("could not find click")
