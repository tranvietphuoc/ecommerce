from logging.config import dictConfig
import pathlib
import yaml
import logging


log_configure_file = (
    pathlib.Path(__file__).parent.parent.joinpath("logging.yaml").resolve()
)
with open(log_configure_file, "r") as l:
    config = yaml.safe_load(l.read())
    dictConfig(config)


logger = logging.getLogger(__name__)
