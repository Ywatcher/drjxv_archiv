from urllib.request import urlopen
from typing import List

# 导入BeautifulSoup
from bs4 import BeautifulSoup as bf
from bs4.element import Tag



def zhihu_question_url(question_id) -> str:
    return "https://www.zhihu.com/question/{}".format(question_id)
def zhihu_answer_url(answer_id) -> str:
    return "https://www.zhihu.com/answer/{}".format(answer_id)


# 导入urllib库的urlopen函数

# 发出请求，获取html
# url = "https://www.baidu.com/"
class Author:
    pass
class Answer:
    def __init__(
        self, 
        data_za_index:int,
        author_name:str,
        answer_id:int,
        itemprop: str,
        meta:List[Tag],
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
        url = zhihu_answe
        pass
def parse_answer_block_from_question(answer:Tag):
    index = answer.get("data-za-index")
    data_zop_dict = ast.literal_eval(answers[0].get("data-zop"))
    author_name = data_zop_dict["authorName"]
    answer_id = data_zop_dict["itemId"]
    itemprop = answer.get("itemprop")
    meta = answer.find_all("meta") 
    return Answer(
        data_za_index=index,
        author_name=author_name,
        answer_id=answer_id,
        itemprop=itemprop,
        meta= meta,
    )
# 打印html内容
# print(html_text)

# 请求获取HTML

# 导入urllib库的urlopen函数

# 发出请求，获取html
# url = "https://www.baidu.com/"
url = zhihu_question_url(20785173)
html = urlopen(url)
# 获取的html内容是字节，将其转化为字符串
html_text = bytes.decode(html.read())
# 打印html内容
# print(html_text)

# 请求获取HTML

# 用BeautifulSoup解析html
obj = bf(html_text, 'html.parser')
title = obj.head.title
# 打印标题
print(title)
answers = obj.find_all('div',class_="ContentItem AnswerItem")