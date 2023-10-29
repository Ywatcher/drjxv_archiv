from data_handler.database import DataBase
from git import Repo
import os


def init_archiv(
    git_repo_path: str,
    db_path: str,
    overwrite: bool = True
):
    if overwrite:
        if os.path.exists(db_path):
            os.remove(db_path)
    DataBase.init_database(db_path)
    if not os.path.exists(git_repo_path):
        raise NotImplemented
    else:
        repo = Repo(git_repo_path)
        # TODO:
        # if not commits: make one commit
    with DataBase(db_path) as db:
        db.update_git_head(
            repo.head.object.hexsha, to_commit=True
        )
