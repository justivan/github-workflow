import os
import pathlib
import sys
import nest_asyncio

NOTEBOOKS_DIR = pathlib.Path(__file__).parent
REPO_DIR = NOTEBOOKS_DIR.parent.parent
DJANGO_PROJECT_ROOT = REPO_DIR / "app"
DJANGO_SETTINGS_MODULE = "core.settings"

def init(verbose=False):
    try:
        nest_asyncio.apply()
        if verbose:
            print("Applied nest_asyncio patch for Jupyter compatibility")
    except ImportError:
        if verbose:
            print("nest_asyncio not available, skipping patch")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    if str(DJANGO_PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(DJANGO_PROJECT_ROOT))
        if verbose:
            print(f"Added {DJANGO_PROJECT_ROOT} to sys.path")

    try:
        import django
        django.setup()
        if verbose:
            print("Django environment initialized successfully")
    except Exception as e:
        if verbose:
            print(f"Error initializing Django: {str(e)}")

    if verbose:
        from django.db import connections
        from django.db.utils import OperationalError

        try:
            connection = connections['default']
            cursor = connection.cursor()
            cursor.execute("SELECT 1;")
            if verbose:
                print("Database connection test: SUCCESS")
        except OperationalError as e:
            if verbose:
                print(f"Database connection test: FAILED with error {str(e)}")
