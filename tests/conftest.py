# Core Library
import logging


def pytest_configure(config):
    """Flake8 is very verbose by default. Silence it."""
    logging.getLogger("flake8").setLevel(logging.WARNING)
