from git.util import Actor
from datetime import datetime
import os
from git import Repo
from typing import Optional


class GitOperator:
    from git.objects.commit import Commit

    @staticmethod
    def create_repo(repo_path: str):
        raise NotImplementedError

    def __init__(
        self,
        repo_path: str,
        commiter_name: str,
        commiter_email: str,
    ):
        """
        :param commiter_name: name of recorder of this repo
        :param commiter_email: url of recorder of this repo
        :param repo_path: absolute path of this repo, should be a git repo
        """
        self.repo_path = repo_path
        self.repo = Repo(repo_path)
        self.commiter = Actor(name=commiter_name, email=commiter_email)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        pass

    def commit_file(
        self,
        file_name: str,
        message: str,
        modified_datetime: datetime,
        fetched_datetime: datetime,
        author_name: str = "unknown",
        author_url: str = "unknown",
        parent_sha: Optional[str] = None
    ) -> Commit:
        """
        :param file_name: relative name to repo
        :param message: commit message
        :param modified_datetime
        :param fetched_datetime
        """
        # TODO: assert path is relative
        # file name should be {answer/question}_{id}
        file_path_full = os.path.join(self.repo_path, file_name)
        self.repo.git.add(file_path_full)
        author = Actor(name=str(author_name), email=str(author_url))
        try:
            parent_commit = self.get_commit_by_sha(parent_sha)
        except BaseException:
            parent_commit = self.repo.head.commit
        self.repo.index.commit(
            parent_commits=[parent_commit],
            message=message,
            author=author,
            committer=self.commiter,
            commit_date=fetched_datetime,
            author_date=modified_datetime
        )
        return self.repo.head.commit

    def get_commit_by_sha(
        self,
        sha: str
    ) -> Commit:
        """
        :param sha: full hexsha str of this commit
        """
        commits = list(self.repo.iter_commits(
            sha, "",
            # ancestry_path=True
        ))[0]
        return commits

    def show_file_at_version(
        self,
        sha: str,
        file_name: str
    ) -> str:
        """
        :param sha: full or partial shahex of commit
        :param filename: filename without prefix
        """
        return self.repo.git.show(
            "{}:{}".format(sha, file_name)
        )

    def file_diff_with_version(
        self,
        sha: str,
        file_name: str,
        file_content: str
    ) -> bool:
        prev_content = self.show_file_at_version(
            sha=sha,
            file_name=file_name
        )
        return prev_content == file_content

    def get_full_name(self, file_name) -> str:
        return os.path.join(self.repo_path, file_name)

    def revert_commit(self, sha):
        raise NotImplemented
