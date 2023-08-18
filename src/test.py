import os.path
from urllib.request import urlopen
from typing import List
import ast
# 导入BeautifulSoup
from bs4 import BeautifulSoup as bf
from bs4.element import Tag
from util.repo import root
import xmltojson


def zhihu_question_url(question_id) -> str:
    return "https://www.zhihu.com/question/{}".format(question_id)


def zhihu_answer_url(answer_id) -> str:
    return "https://www.zhihu.com/answer/{}".format(answer_id)


class Author:
    pass


class Question:
    def __init__(
            self,
            question_id: int = None,
            title: str = None,
            meta:List[Tag]=None,
            answers=None
    ):
        self.title = title
        self.question_id = question_id
        self.answers = answers
        self.meta = meta

    def parse(self, recurse: bool, text=None):
        print("parsing question")
        if text is None:
            url = zhihu_question_url(self.question_id)
            html = urlopen(url)
            # 获取的html内容是字节，将其转化为字符串
            html_text = bytes.decode(html.read())
        else:
            html_text = text
        # 用BeautifulSoup解析html
        obj = bf(html_text, 'html.parser')
        if self.title is None:
            self.title = obj.head.title.text
        question_info = obj.find('div',class_='QuestionPage')
        if self.question_id is None:
            # for example data-za-extra-module='{"card":{"content":{"type":"Question","token":"532925796"}}}'
            data_za_extra_module_dict = ast.literal_eval(question_info.get('data-za-extra-module'))
            self.question_id = int(data_za_extra_module_dict["card"]["content"]["token"] )
        print("\twith question id={}".format(self.question_id))
        print("\ttitle:{}".format(self.title))
        if self.meta is None:
            self.meta = question_info.find_all("meta")
        if self.answers is None:
            # self.list = obj.find_all('div', class_="List-item")
            answer_blocks = obj.find_all('div', class_="ContentItem AnswerItem")
            self.answers = [
                parse_answer_block_from_question(answer, recurse=recurse)
                for answer in answer_blocks
            ]


class Answer:
    def __init__(
            self,
            data_za_index: int,
            author_name: str,
            answer_id: int,
            itemprop: str,
            meta: List[Tag],
            content=None,
            comments=None
    ):
        self.data_za_index = data_za_index
        self.author_name = author_name
        self.answer_id = answer_id
        self.itemprop = itemprop
        self.content = content
        self.comments = comments
        self.meta = meta

    def get_content_and_comment(self):
        print("\t\tparsing answer with id={}".format(self.answer_id))
        # 发出请求，获取html
        url = zhihu_answer_url(self.answer_id)
        html = urlopen(url)
        # 获取的html内容是字节，将其转化为字符串
        html_text = bytes.decode(html.read())
        # 用BeautifulSoup解析html
        obj = bf(html_text, 'html.parser')
        # self.p = obj.find('p')
        # self.content: a list of paragraphs and figures
        self.content = obj.find('div', class_='RichContent-inner').find('span').contents

    def __repr__(self):
        return "Answer(id={})".format(self.answer_id)

class Paragraph:
    def __init__(self, text):
        self.text = text

def parse_answer_block_from_question(answer_block: Tag, recurse: bool):
    index = int(answer_block.get("data-za-index"))
    data_zop_dict = ast.literal_eval(answer_block.get("data-zop"))
    author_name = data_zop_dict["authorName"]
    answer_id = data_zop_dict["itemId"]
    itemprop = answer_block.get("itemprop")
    meta = answer_block.find_all("meta")
    answer = Answer(
        data_za_index=index,
        author_name=author_name,
        answer_id=answer_id,
        itemprop=itemprop,
        meta=meta,
    )
    if recurse:
        answer.get_content_and_comment()
    return answer


if __name__ == "__main__":
    question_id = 20785173
    # question = Question(question_id=question_id)
    # question.parse(recurse=False)
    # file_name = "如何评价俄罗斯的T90m坦克？ - 知乎.html"
    file_name = "如何评价俄罗斯的T90m坦克？ - 知乎.html"
    with open(os.path.join(root, file_name)) as f:
        s = f.read()
    question = Question()
    question.parse(recurse=True, text=s)
    print(question.answers[0].content)
