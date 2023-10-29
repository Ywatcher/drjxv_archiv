from multiprocessing import Queue
from common import QuestionBriefInfo, AnswerParseTask, TaskStopEvent
from bs4 import BeautifulSoup as bf
from selenium.common.exceptions import ElementNotVisibleException
from util.web_util import zhihu_question_url, close_button, expand_question


class QuestionParser:
    def __init__(
        self,
        queue_put_result: Queue,
        queue_put_task: Queue,
        driver,
        logger=None
    ):
        self.queue_put_result = queue_put_result
        self.queue_put_task = queue_put_task
        self.driver = driver
        self.logger = logger

    def parse(self, question_id, single_parse=True):
        if self.logger is not None:
            self.logger.log(
                f"parsing question with id={question_id}")
        url = zhihu_question_url(question_id)
        try:
            self.driver.get(url)
            close_button(self.driver)
        except ElementNotVisibleException:
            print("try again")
            # FIXME: close f12
            self.driver.get(url)
            close_button(self.driver)
        expand_question(self.driver)
        # self.driver.get(url)
        answerCount = self.driver.find_element_by_xpath(
            '//div[@class="QuestionPage"]/meta[@itemprop="answerCount"]'
        ).get_attribute("content")
        dateCreated = self.driver.find_element_by_xpath(
            '//div[@class="QuestionPage"]/meta[@itemprop="dateCreated"]'
        ).get_attribute("content")
        dateModified = self.driver.find_element_by_xpath(
            '//div[@class="QuestionPage"]/meta[@itemprop="dateModified"]'
        ).get_attribute("content")

        content_blocks = self.driver.find_elements_by_xpath(
            '//div[@class="QuestionHeader"]'
        )
        # assert len(content_blocks)==1
        content_block = content_blocks[0].get_attribute("outerHTML")
        # parse content(rich text) and title
        parsed_question_info = self.parse_question_block(content_block)
        self.queue_put_result.put(QuestionBriefInfo(
            question_id=question_id,
            answerCount=answerCount,
            dateCreated=dateCreated,
            dateModified=dateModified,
            **parsed_question_info
        ))
        self.put_answer_tasks_to_queue(question_id, single_parse)

    @staticmethod
    def parse_question_block(html_text: str):
        obj = bf(html_text, 'html.parser')
        title = obj.find('h1', class_="QuestionHeader-title").text
        content = obj.find(
            'div',
            class_="QuestionRichText QuestionRichText--expandable"
        ).find('span').contents

        return {
            "title": title,
            "content": content
        }

    def put_answer_tasks_to_queue(self, question_id, single_parse=True):
        # FIXME: scroll
        question_answers = self.driver.find_elements_by_xpath(
            '//div[@class="ContentItem AnswerItem"]'
        )
        # TODO: scroll and catch new items loaded
        for q in question_answers:
            self.queue_put_task.put(
                AnswerParseTask(
                    question_id=question_id,
                    answer_id=q.get_attribute("name")
                )
            )
        if single_parse:
            self.queue_put_task.put(TaskStopEvent())
            self.driver.close()

    def start_parsing_list(self, question_id_list: list):
        for question_id in question_id_list:
            print(question_id)
            self.parse(question_id, single_parse=False)
            print("parsed",question_id)
        print("fin")
        self.queue_put_task.put(TaskStopEvent())
        self.driver.close()
