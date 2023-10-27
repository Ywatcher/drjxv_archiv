from dataclasses import dataclass
from typing import Union, Dict


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


@dataclass
class AnswerParseTask:
    question_id: Union[int, str]
    answer_id: Union[int, str]


class TaskStopEvent:
    pass
