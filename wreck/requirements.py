# This is an especially simple version of requirements parsing; we do the simple
# thing here to avoid extra deps or fragile APIs, at the expense of missing some
# deps and false-positives.

from pathlib import Path
from typing import Iterator, Tuple

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name


def iter_simple_requirements(path: Path) -> Iterator[Requirement]:
    for line in path.read_text().splitlines():
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        yield Requirement(line)
