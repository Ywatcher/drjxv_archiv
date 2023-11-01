# -*- coding: utf-8 -*-

import os
from pathlib import Path

# absolute path to project repository
# this variable offers a absolute manner to define relative location
# in this project.
project_root = Path(__file__).parent.parent.absolute()

# path to web_driver
# Please modify the dict `drivers` to designate the path to web driver images;
# You can use `os.path.join` to avoid confusion between Windows style and
# Unix style path strings.
driver_root = os.path.join(project_root, "driver")

drivers = {
    "chrome": os.path.join(
        driver_root,
        "chromedriver-linux64",
        # "/home/ywatcher/.cache/selenium/chromedriver/linux64/118.0.5993.70",
        "chromedriver"),

    "firefox": os.path.join(
        driver_root, "geckodriver-v0.33.0-linux64", "geckodriver"),
    "edge": os.path.join(
        driver_root, "edgedriver_linux64", "msedgedriver")
}


# The whole repository of archiv consists of different parts, including a
# sqlite3 database file, a git repository to manage different versions of
# answers and questions, and a configuration file of the archiv repository,
# which tells the information about the repo, including the name and email
# of who fetches data to this repo.
# Following functions get_vcs_path(), get_db_path() and get_config_path()
# gives absolute paths to these parts, given the absolute path to root of
# archiv repository.
# You can modify these functions to customize these paths.
# .
# ├── config.yaml
# ├── sqlite_database.db
# └── vcs
#     ├── .git
#     ├── question_xxxx.md
#     ├── answer_xxxx.md
#     └── ...
def get_vcs_path(archiv_repo_path: str) -> str:
    """
    get absolute path of vcs folder, given the absolute path of the
    root of archiv repository.
    """
    return os.path.join(archiv_repo_path, "vcs")


def get_db_path(archiv_repo_path: str) -> str:
    """
    get absolute path of sqlite3 database, given the absolute path of the
    root of archiv repository.
    """
    return os.path.join(archiv_repo_path, "sqlite_database.db")


def get_config_path(archiv_repo_path: str) -> str:
    """
    get absolute path of config file, given the absolute path of the
    root of archiv repository.
    """
    return os.path.join(archiv_repo_path, "config.yaml")


# From answer_file_format() and question_file_format() offer the naming
# convention of file storage for parsed answers and questions, given their
# ids.
# You can customize the convention by modify these functions
def answer_file_format(aid) -> str:
    """
    format answer file name given the id of answer
    """
    return f"answer_{aid}.md"


def question_file_format(qid) -> str:
    """
    format question file name given the id of question
    """
    return f"question_{qid}.md"


# default user that owns the archiv repository.
# These default settings will be used if they are not explicitty passed as
# parameters when creating a new archiv repository.
default_owner_name = "me"
default_owner_email = "me@email"

# numbers of answer parser processes
nr_answer_parsers = 3
if __name__ == "__main__":
    print(project_root)
