from web_parser import AnswerParser, QuestionParser
import multiprocessing
from multiprocessing import Queue, Process
from selenium import webdriver
from pathlib import Path
import os
from util.repo import driver_root, database_root, drivers, git_repo_test

q_id = 625769474
q_list = [q_id]
config = {
    "simutaneously_scrap_and_store": False,
    "nr_answer_scapers": 1
}


class Logger:
    def __init__(self, s: str):
        self.s = s

    def log(self, s):
        print("{}:{}".format(self.s, s))

class EmptyQueue:
    def put(self, *args):
        pass

    def get(self, *args):
        pass

q_task = Queue()
q_result = Queue(maxsize=10000)
# q_result = EmptyQueue()

question_driver = webdriver.Chrome(drivers["chrome"])
question_parser = QuestionParser(
    queue_put_result=q_result,
    queue_put_task=q_task,
    driver=question_driver,
    logger=Logger("q")
)
answer_drivers = []
answer_parsers = []
for i in range(config["nr_answer_scapers"]):
    answer_drivers.append(
        webdriver.Chrome(drivers["chrome"])
    )
    answer_parsers.append(
        AnswerParser(
            queue_put_result=q_result,
            queue_get_task=q_task,
            driver=answer_drivers[i],
            logger=Logger("a_{}".format(i))
        )
    )

if not config["simutaneously_scrap_and_store"]:
    print("scrap, then store")
    targets = [
        # target func and args
        (question_parser.start_parsing_list, (q_list,))
    ] + [
        (answer_parser.start_parsing, [])
        for answer_parser in answer_parsers
    ]

    processes = [
        Process(target=target_func, args=args)
        for target_func, args in targets
    ]


else:
    print(1)

for p in processes:
    p.start()

# for p in processes:
    # p.join()
    # print("join")
    # p.close()
    # print("close")
# print("sdf")
processes[0].join()
processes[0].close()

