from pathlib import Path
from typing import Dict, Optional, Set

import click

import trailrunner
from stdlibs import stdlib_module_names

from .distinfo import iter_all_distinfo_dirs, iter_distinfo_dirs

from .distinfo_inference import analyze, iterparents

from .import_parser import get_imports
from .requirements import iter_glob_all_requirement_names

STDLIB_MODULE_NAMES = stdlib_module_names()  # for the running version only


@click.command()
@click.option(
    "--requirements",
    default="requirements*.txt",
    help="Patterns for finding files from which to read requirements (comma-separated)",
    show_default=True,
)
@click.option("--verbose", "-v", is_flag=True, help="Show more logging")
@click.option("--installed-path", help="Where to look for distinfo if not sys.path")
@click.option(
    "--allow-names",
    help="Minimal names to consider satisfied, such as the current project top-level name (comma-separated)",
)
@click.argument("target_dir")
def main(
    requirements: str,
    target_dir: str,
    installed_path: str,
    allow_names: Optional[str],
    verbose: bool,
) -> None:
    available_names: Dict[str, Optional[str]] = {}
    requirement_names: Set[Optional[str]] = {None}

    # Part 1
    requirement_names = set(iter_glob_all_requirement_names(requirements))

    # Part 2
    if not installed_path:
        for (p, v, d) in iter_all_distinfo_dirs():
            dist = analyze(d)
            for name in dist.minimal_names:
                available_names[name] = p
    else:
        for (p, v, d) in iter_distinfo_dirs(Path(installed_path)):
            dist = analyze(d)
            for name in dist.minimal_names:
                available_names[name] = p

    # Part 2b (first-party names, even if they're installed)
    if allow_names:
        for name in allow_names.split(","):
            available_names[name] = None

    # Part 3
    for path in trailrunner.walk(Path(target_dir)):
        if verbose:
            print(f"{path}:")
        imports = get_imports(path)
        for i in sorted(imports):
            if i in available_names or any(
                x in available_names for x in iterparents(i)
            ):
                providers = []
                for name in (i,) + tuple(iterparents(i)):
                    if name in available_names:
                        providers.append(available_names[name])
                if not all(p in requirement_names for p in providers):
                    if len(providers) == 1:
                        click.echo(
                            f"{path.as_posix()} uses "
                            + click.style(i, bold=True)
                            + " but "
                            + click.style(repr(providers[0]), bold=True)
                            + " not in requirements"
                        )
                    else:
                        click.echo(
                            f"{path.as_posix()} uses "
                            + click.style(i, bold=True)
                            + " but "
                            + click.style(repr(providers), bold=True)
                            + " not all in requirements"
                        )
                if verbose:
                    print(f"  {i} available from {providers}")
            elif i.split(".")[0] in STDLIB_MODULE_NAMES:
                if verbose:
                    print(f"  {i} stdlib")
            else:
                click.echo(
                    f"{path.as_posix()} uses "
                    + click.style(i, bold=True)
                    + " but there is nothing installed to provide it"
                )


if __name__ == "__main__":
    main()
