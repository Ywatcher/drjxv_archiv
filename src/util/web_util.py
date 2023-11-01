# -*- coding: utf-8 -*-
import time
from typing import Callable, Optional
from util.logger import BaseLogger


def zhihu_question_url(question_id) -> str:
    return "https://www.zhihu.com/question/{}".format(question_id)


def zhihu_answer_url(answer_id) -> str:
    return "https://www.zhihu.com/answer/{}".format(answer_id)


def close_button(driver):
    """
    to close the popup when entering a page
    """
    close_buttons = driver.find_elements_by_xpath(
        # "Button Modal-closeButton Button--plain"
        '//button[@class="Button Modal-closeButton Button--plain"]'
    )
    assert len(close_buttons) == 1
    close_buttons[0].click()


def expand_question(driver):
    expand_button = None
    try:
        all_buttons = driver.find_element_by_xpath(
            '//div[@class="QuestionHeader-content"]'
        ).find_element_by_xpath(
            '//div[@class="QuestionRichText QuestionRichText--expandable QuestionRichText--collapsed"]'
        ).find_elements_by_xpath("//button")
        # FIXME: do not press if button does not exist
        assert all_buttons[5].text == '显示全部'
        expand_button = all_buttons[5]
    # for b in all_buttons:
    #     b.text
    #     if b.text == '显示全部':
    #         print(b.text)
    #         expand_button = b
    #     break
        expand_button.click()
    except Exception as e:
        # FIXME : if no such button
        pass


# modified from
# https://www.cnblogs.com/moneymaster/p/14606132.html
def scroll_to_bottom(
    driver,
    get_sleep_time: Callable[..., float] = lambda: 5,  # FIXME,
    logger: Optional[BaseLogger] = None
):
    js = 'return document.body.scrollHeight;'
    height = 0
    while True:
        new_height = driver.execute_script(js)
        if new_height > height:
            driver.execute_script(
                'window.scrollTo(0, document.body.scrollHeight)')
            height = new_height
            sleep_time = get_sleep_time()
            time.sleep(sleep_time)
        else:
            if logger is not None:
                logger.log("Scrolled to bottom.")
            driver.execute_script('window.scrollTo(0, 0)')  # scrolled to bot
            break
