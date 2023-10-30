# -*- coding: utf-8 -*-

from data_handler.database import DataBase
from git import Repo
import os
from util.repo import get_db_path, get_vcs_path


def make_abs(path: str) -> str:
    if os.path.isabs(path):
        return path
    else:
        p = os.path.normpath(os.path.join(os.getcwd(), path))
        return p


def init_new_repo(
    repo_path: str,
    author: str,
    logger=None
):
    repo_path = make_abs(repo_path)
    try:
        assert not os.path.exists(repo_path)
    except Exception as e:
        raise FileExistsError("Path {} already exists.".format(repo_path))

    os.mkdir(repo_path)
    if logger is not None:
        logger.log(f"created dir: {repo_path}")
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
            author=author
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
    from util.repo import root
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
