# There are multiple projects that can answer the same questions this module
# does, but they are generally complex and have complex deps.
#
# For the goal of running this against a venv on CI, we don't need any of that
# and can rely on files being materialized on disk.

import re
import sys
from pathlib import Path
from typing import Iterator, Tuple

from packaging.utils import canonicalize_name

DISTINFO_RE = re.compile(r"([^-]+)-(.*?)\.dist-info$")


def iter_all_distinfo_dirs() -> Iterator[Tuple[str, str, Path]]:
    for p in sys.path:
        path = Path(p)
        if path.is_dir():
            yield from iter_distinfo_dirs(path)


def iter_distinfo_dirs(path: Path) -> Iterator[Tuple[str, str, Path]]:
    for subdir in path.iterdir():
        if subdir.name.endswith(".dist-info") and subdir.is_dir():
            # TODO error handling
            (project, version) = DISTINFO_RE.match(subdir.name).groups()

            # Change from underscores to dashes
            project = canonicalize_name(project)

            yield project, version, subdir


if __name__ == "__main__":
    for x in iter_all_distinfo_dirs():
        print(x)
