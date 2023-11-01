# -*- coding: utf-8 -*-

from os.path import isdir
from pathlib import Path
from typing import Optional
from data_handler.database import DataBase
from git import Repo
import os
from config import get_config_path, get_db_path, get_vcs_path, get_config_path
from config import default_owner_email, default_owner_name
from util.file_rendering import to_config_file


def make_abs(path: str) -> str:
    if os.path.isabs(path):
        return path
    else:
        p = os.path.normpath(os.path.join(os.getcwd(), path))
        return p


def init_new_repo(
    repo_path: str,
    owner_name: Optional[str] = None,
    owner_email: Optional[str] = None,
    logger=None
):

    repo_path = make_abs(repo_path)
    if owner_name is None:
        owner_name = default_owner_name
    if owner_email is None:
        owner_email = default_owner_email
    owner = "{}<{}>".format(owner_name, owner_email)
    if os.path.exists(repo_path):
        if not os.path.isdir(repo_path):
            raise NotADirectoryError(
                f"{repo_path} exists, and is not a directory")
        elif len(os.listdir(repo_path)) > 0:
            raise OSError(
                f"{repo_path} exists, and is not empty"
            )
    else:
        parent_path = Path(repo_path).parent
        if not os.path.exists(parent_path):
            raise FileNotFoundError(
                f"path:{parent_path} not found")
        elif not os.path.isdir(parent_path):
            raise NotADirectoryError(
                f"{parent_path} is not a directory"
            )
    # create a new repo
    os.mkdir(repo_path)
    if logger is not None:
        logger.log(f"created dir: {repo_path}")
    # write to config file
    with open(get_config_path(repo_path), "w") as config_file:
        file_content = to_config_file(owner_name, owner_email)
        config_file.write(file_content)
    # init vcs and db
    vcs_path = get_vcs_path(repo_path)
    db_path = get_db_path(repo_path)
    os.mkdir(vcs_path)
    # os.mkdir(db_path)
    DataBase.init_database(db_path)
    if logger is not None:
        logger.log(f"database initialized: {db_path}")
    repo = Repo.init(vcs_path, bare=False)
    if logger is not None:
        logger.log(f"git repo created: {vcs_path}")
    try:
        repo.git.config(
            "--global", "--add", "safe.directory", vcs_path)
        repo.git.commit(
            "--allow-empty", "-m", "create_repo",
            author=owner
        )
        with DataBase(db_path) as db:
            db.update_git_head(
                repo.head.object.hexsha, to_commit=True
            )
        if logger is not None:
            logger.log(f"initialized git head: {repo.head.object.hexsha}")
    except Exception as e:
        raise e


def main():
    from config import project_root
    repo_path = "../../test_repo_3"
    author = "test<test>"
    init_new_repo(repo_path, author)


if __name__ == "__main__":
    main()
    # p=   os.path.normpath( os.path.join(
    # os.getcwd(),
    # "../../test"
    # )
    # )
