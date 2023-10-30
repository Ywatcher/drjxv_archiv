# -*- coding: utf-8 -*-

import os
from pathlib import Path

# path to code repository
root = Path(__file__).parent.parent.parent.absolute()
driver_root = os.path.join(root, "driver")
# path to web_driver

drivers = {  # FIXME: put it into config
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


# path to archiv repository
# .
# ├── .database
# │   └── sqlite_data.db
# └── vcs
#     ├── ...
#     ├── answer_xxxx.md
#     ├── .git
#     └── question_xxxx.md

def get_vcs_path(archiv_repo_path: str) -> str:
    return os.path.join(archiv_repo_path, "vcs")


def get_db_path(archiv_repo_path: str) -> str:
    return os.path.join(archiv_repo_path, ".sqlite_database.db")


def answer_file_format(aid) -> str:
    return f"answer_{aid}.md"


def question_file_format(qid) -> str:
    return f"question_{qid}.md"


if __name__ == "__main__":
    print(root)
