from dataclasses import dataclass
from typing import Union, Dict
from util.file_rendering import to_markdown, tags_to_str
from util.time import str2date
import datetime

from bs4.element import Tag
# TODO: mv to util




@dataclass
class AnswerBriefInfo:
    question_id: str
    answer_id: str
    author: str
    content: list[Tag]  # html like
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
            content=tags_to_str(self.content)
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
    content: list[Tag]
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
            content=tags_to_str(self.content)
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
