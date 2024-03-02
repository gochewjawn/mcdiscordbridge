from contextlib import contextmanager
from dataclasses import dataclass
from logging import getLogger
from pathlib import Path
from json import dump, load

_logger = getLogger(__name__)


@dataclass
class Database:
    consumer_channel_ids: list[int]
    producer_channel_ids: list[int]


def load_database_data(path: str) -> Database:
    _logger.info("Loading database file")
    try:
        with open(path, "r") as file:
            return Database(**load(file))
    except FileNotFoundError:
        _logger.info("Falling back to default database data")
        return Database(consumer_channel_ids=[], producer_channel_ids=[])


def save_database_data(database: Database, path: str) -> None:
    _logger.info("Writing database to disk")
    with Path(path) as path_obj:
        path_obj.parent.mkdir(parents=True, exist_ok=True)
        with path_obj.open("w") as file:
            dump(database.__dict__, file, indent=4)


@contextmanager
def load_database(path: str):
    database = load_database_data(path)
    yield database
    save_database_data(database, path)
