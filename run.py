import os
import yaml
import logging

from config import ROOT_DIR, HOST, PORT, DEBUG
from src.index import app


def setup_logging() -> None:
    with open(os.path.join(ROOT_DIR, "logging.yaml"), "rt") as log_file:
        config = yaml.safe_load(log_file.read())
    logging.config.dictConfig(config)


setup_logging()


if __name__ == "__main__":
    app.run(host=HOST,
            port=PORT,
            debug=DEBUG)
