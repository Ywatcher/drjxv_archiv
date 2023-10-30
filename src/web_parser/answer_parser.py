# -*- coding: utf-8 -*-

from multiprocessing import Queue
from common import AnswerBriefInfo, AnswerParseTask, TaskStopEvent
from typing import List, Dict
from bs4 import BeautifulSoup as bf
from selenium.common.exceptions import ElementNotVisibleException
from util.web_util import zhihu_answer_url, close_button
from time import sleep


class AnswerParser:
    def __init__(
        self,
        queue_get_task: Queue,
        queue_put_result: Queue,
        driver,
        logger=None
    ):
        self.queue_get_task = queue_get_task
        self.queue_put_result = queue_put_result
        self.driver = driver
        self.logger = logger

    def parse(self, answer_id, question_id=None):
        self.log(f"parsing answer with id={answer_id}")
        url = zhihu_answer_url(answer_id=answer_id)
        try:
            self.driver.get(url)
            close_button(self.driver)
        except ElementNotVisibleException:
            self.log("try again")
            # FIXME: close f12
            self.driver.get(url)
            close_button(self.driver)
        if question_id is None:
            question_id = ""  # FIXME: get question id from web element
        content_blocks = self.driver.find_elements_by_xpath(
            '//div[@class="QuestionAnswer-content"]'
        )
        assert len(content_blocks) == 1
        content_block = content_blocks[0].find_element_by_xpath(
            '//div[@class="QuestionAnswer-content"]'  # FIXME
        ).get_attribute("outerHTML")

        parsed_answer_info = self.parse_content_block(
            html_text=content_block
        )
        self.queue_put_result.put(AnswerBriefInfo(
            question_id=question_id,
            answer_id=answer_id,
            **parsed_answer_info
        ))
        if False:  # FIXME
            self.get_comments()

    @staticmethod
    def parse_content_block(html_text: str) -> Dict[str, str]:
        obj = bf(html_text, 'html.parser')
        content = obj.find(
            'div', class_='RichContent-inner').find('span').contents
        author = None  # TODO
        upvoteCount = obj.find('meta', itemprop="upvoteCount").get("content")
        dateCreated = obj.find('meta', itemprop="dateCreated").get("content")
        dateModified = obj.find('meta', itemprop="dateModified").get("content")
        commentCount = obj.find('meta', itemprop='commentCount').get("content")
        return {
            "author": author,
            "content": content,
            "upvoteCount": upvoteCount,
            "dateCreated": dateCreated,
            "dateModified": dateModified,
            "commentCount": commentCount
        }

    def get_comments(self):
        pass

    def start_parsing(self):
        while True:
            task = self.queue_get_task.get(True, 10)
            if isinstance(task, TaskStopEvent):
                self.log("stop")
                # may block if without `nowait`
                self.queue_get_task.put_nowait(task)
                self.log("put")
                # to_break = True
                break
            elif isinstance(task, AnswerParseTask):
                self.parse(
                    answer_id=task.answer_id,
                    question_id=task.question_id
                )
            else:
                raise Exception

        self.log("out")
        self.driver.close()  # FIXME

    def log(self, *args, **kwargs):
        if self.logger is not None:
            self.logger.log(*args, **kwargs)
