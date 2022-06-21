import logging
from logging.config import dictConfig
import pathlib
import yaml


# logging.basicConfig(
#     format="%(asctime)s - %(level)s - %(message)s", level=logging.INFO
# )

log_configure_file = (
    pathlib.Path(__file__).parent.parent.joinpath("logging.yaml").resolve()
)
with open(log_configure_file, "r") as l:
    config = yaml.safe_load(l.read())
    dictConfig(config)


logger = logging.getLogger(__name__)

# logging
# create file and stream handler
# stream = logging.StreamHandler()  # for stream handler
# file = logging.FileHandler("app.log")  # for file handler

# # config handler
# # logging level
# stream.setLevel(logging.INFO)
# file.setLevel(logging.INFO)
# # logging formatter
# stream.setFormatter(
#     logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# )
# file.setFormatter(
#     logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# )
#
# # add handler
# logger.addHandler(stream)
# logger.addHandler(file)

