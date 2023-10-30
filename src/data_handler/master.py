# -*- coding: utf-8 -*-

from common import AnswerBriefInfo, QuestionBriefInfo
from typing import Union
from data_handler.database import DataBase
from data_handler.vcs import GitOperator
from multiprocessing import Queue
from util.time import current_time


class Master:
    from git.objects.commit import Commit

    def __init__(
        self,
        db_path: str,
        git_repo_path: str
    ):
        self.db_path = db_path
        self.git_repo_path = git_repo_path

    @staticmethod
    def get_answer_filename(answer_id) -> str:
        return f"answer_{answer_id}.md"

    @staticmethod
    def get_question_filename(question_id) -> str:
        return f"question_{question_id}.md"

    def start_parse(
        self,
        commiter_name: str, commiter_email: str,
        result_queue: Queue
    ):
        with DataBase(self.db_path) as db_instance, \
                GitOperator(
                    self.git_repo_path,
                    commiter_email=commiter_email,
                    commiter_name=commiter_name
                ) as git_repo_insance:
            while not result_queue.empty():
                result = result_queue.get()
                self.handle(
                    result=result,
                    db=db_instance, git_operator=git_repo_insance
                )

    def handle(
        self,
        db: DataBase,
        git_operator: GitOperator,
        result: Union[AnswerBriefInfo, QuestionBriefInfo]
    ):
        if isinstance(result, AnswerBriefInfo):
            answer_id = result.answer_id
            filename = self.get_answer_filename(answer_id)
            file_content = result.to_markdown_()
            to_update = False
            head = db.get_git_head()
            if db.has_answer(answer_id):
                # commit and make a new version
                to_update = git_operator.file_diff_with_version(
                    file_content=file_content,
                    file_name=filename,
                    sha=head
                )
            else:
                db.add_answer(
                    answer_id=int(answer_id),
                    question_id=int(result.question_id),
                    dateCreated=result.dateCreate_d,
                    to_commit=False
                    # FIXME: author id
                )
                to_update = True
            if to_update:
                fetchedDatetime_d = current_time()
                with open(
                    git_operator.get_full_name(filename),
                    "w"
                ) as f:
                    f.write(file_content)
                git_latest_commit = git_operator.commit_file(
                    file_name=filename,
                    message=self.format_answer_commit_message(result),
                    modified_datetime=result.dateModified_d,
                    fetched_datetime=fetchedDatetime_d,
                    parent_sha=head
                    # author = .., author_url=..
                )
                sha = git_latest_commit.hexsha
                try:
                    db.update_git_head(sha=sha, to_commit=False)
                    db.add_answer_version(
                        answer_id=int(answer_id),
                        commit_id=sha,
                        dateFetched=fetchedDatetime_d,
                        dateModified=result.dateModified_d,
                        commentCount=int(result.commentCount),
                        to_commit=True
                    )
                except Exception as e:
                    git_operator.revert_commit(head)
                    db.cancel()
                    raise e

        elif isinstance(result, QuestionBriefInfo):
            question_id = result.question_id
            filename = self.get_question_filename(question_id)
            file_content = result.to_markdown_()
            to_update = False
            head = db.get_git_head()
            if db.has_question(question_id):
                # commit and make a new version
                to_update = git_operator.file_diff_with_version(
                    file_content=file_content,
                    file_name=filename,
                    sha=head
                )
            else:
                db.add_question(
                    question_id=int(question_id),
                    dateCreated=result.dateCreate_d,
                    to_commit=False
                    # FIXME: author id
                )
                to_update = True
            if to_update:
                fetchedDatetime_d = current_time()
                with open(
                    git_operator.get_full_name(filename),
                    "w"
                ) as f:
                    f.write(file_content)
                git_latest_commit = git_operator.commit_file(
                    file_name=filename,
                    message=self.format_question_commit_message(result),
                    modified_datetime=result.dateModified_d,
                    fetched_datetime=fetchedDatetime_d,
                    parent_sha=head
                    # author = .., author_url=..
                )
                sha = git_latest_commit.hexsha
                try:
                    db.update_git_head(sha=sha, to_commit=False)
                    db.add_question_version(
                        question_id=int(question_id),
                        commit_id=sha,
                        dateFetched=fetchedDatetime_d,
                        dateModified=result.dateCreate_d,
                        answerCount=int(result.answerCount),
                        to_commit=True
                    )
                except Exception as e:
                    git_operator.revert_commit(head)
                    db.cancel()
                    raise e
        else:
            raise NotImplementedError

    @staticmethod
    def format_answer_commit_message(answer: AnswerBriefInfo) -> str:
        aid = answer.answer_id
        qid = answer.question_id
        text = answer.content[0].text
        if len(text) >= 30:
            text = text[:50] + "..."
        return "answer `{}`({}) from question {}".format(
            text, aid, qid
        )

    @staticmethod
    def format_question_commit_message(question: QuestionBriefInfo) -> str:
        qid = question.question_id
        title = question.title
        return "question `{}`({})".format(title, qid)

    @staticmethod
    def format_commit_message(
            result: Union[QuestionBriefInfo, AnswerBriefInfo]) -> str:
        if isinstance(result, QuestionBriefInfo):
            return Master.format_question_commit_message(result)
        elif isinstance(result, AnswerBriefInfo):
            return Master.format_answer_commit_message(result)
        else:
            raise TypeError
