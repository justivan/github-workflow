import sys
import pathlib
import os
import nest_asyncio


def init(verbose=False):
    workspace = pathlib.Path(__file__).resolve().parents[1]
    project_root = workspace / "app"

    try:
        nest_asyncio.apply()
        if verbose:
            print("Applied nest_asyncio patch for Jupyter compatibility")
    except ImportError:
        if verbose:
            print("nest_asyncio not available, skipping patch")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        if verbose:
            print(f"Added {project_root} to sys.path")

    import django

    django.setup()


if __name__ == "__main__":
    init()
