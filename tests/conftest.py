import logging


def pytest_configure(config):
    """Flake8 is very verbose by default. Silence it."""  # noqa: DAR101
    logging.getLogger("flake8").setLevel(logging.ERROR)
