from dataclasses import dataclass
from typing import Union, Dict
from util.file_rendering import to_markdown
import datetime

# TODO: mv to util


def str2date(strdate: str) -> datetime.datetime:
    # format: "%Y-%m-%dT%H:%M:%S.%fZ"
    # example: "2023-10-13T18:14:15.000Z"
    return datetime.datetime.fromisoformat(strdate)


@dataclass
class AnswerBriefInfo:
    question_id: str
    answer_id: str
    author: str
    content: str  # html like
    upvoteCount: Union[int, str]
    dateCreated: str
    dateModified: str
    commentCount: str

    def to_markdown_(self) -> str:
        return to_markdown(
            metadata={
                "type": "answer",
                "answer_id": self.answer_id,
                "author": self.author,
                "dateCreated": self.dateCreated,
                "upvoteCount": self.upvoteCount,
                "commentCount": self.commentCount
            },
            title=None,
            content=self.content
        )

    @property
    def dateCreate_d(self) -> datetime.datetime:
        return str2date(self.dateCreated)

    @property
    def dateModified_d(self) -> datetime.datetime:
        return str2date(self.dateModified)


@dataclass
class CommentBriefInfo:
    pass


@dataclass
class QuestionBriefInfo:
    question_id: str
    title: str
    content: str
    answerCount: str
    dateCreated: str
    dateModified: str

    def to_markdown_(self) -> str:
        return to_markdown(
            metadata={
                "type": "question",
                "question_id": self.question_id,
                "dateCreated": self.dateCreated,
                "answerCount": self.answerCount,
                "title": self.title
            },
            title=self.title,
            content=self.content
        )

    @property
    def dateCreate_d(self) -> datetime.datetime:
        return str2date(self.dateCreated)

    @property
    def dateModified_d(self) -> datetime.datetime:
        return str2date(self.dateModified)


@dataclass
class AnswerParseTask:
    question_id: Union[int, str]
    answer_id: Union[int, str]


class TaskStopEvent:
    pass
