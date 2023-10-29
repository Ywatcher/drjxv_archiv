import datetime
import sqlite3
from sqlite3 import Error
from util.db import is_empty
# answer_table:
title_4_answer_table = "Answers"
title_4_question_table = "Questions"
title_4_comment_table = "Comments"
query_create_answer_table = f"""
CREATE TABLE IF NOT EXISTS {title_4_answer_table} (
    id integer PRIMARY KEY,
    authorId integer,
    questionId integer NOT NULL,
    dateCreated text
    )
"""
query_create_answer_vcs_table = f"""
CREATE TABLE IF NOT EXISTS {title_4_answer_table}VCS (
    commitId text PRIMARY KEY,
    answerId interger NOT NULL,
    dateFetched text,
    dateModified text,
    commentCount integer
    )
"""
query_create_question_table = f"""
CREATE TABLE IF NOT EXISTS {title_4_question_table} (
    id integer PRIMARY KEY,
    authorId integer,
    dateCreated text
    )
"""
query_create_question_vcs_table = f"""
CREATE TABLE IF NOT EXISTS {title_4_question_table}VCS (
    commitId text PRIMARY KEY,
    questionId interger NOT NULL,
    dateFetched text,
    dateModified text,
    answerCount integer
    )
"""
# create a table named GitHead
# to maintain the current head
# of git repository, sha of
# which is stored;
# This table aims to prevent
# unexpected effects caused by
# manual git operations
query_create_head_table = f"""
CREATE TABLE IF NOT EXISTS GitHead(
    id INTEGER PRIMARY KEY CHECK (id = 0),
    sha text
);
CREATE TRIGGER IF NOT EXISTS git_head_no_insert
BEFORE INSERT ON GitHead
WHEN (SELECT COUNT(*) FROM GitHead) >= 1   -- limit here
BEGIN
    SELECT RAISE(FAIL, 'only one row!');
END;
"""


def init_database_tables(
    conn: sqlite3.Connection
) -> int:
    # TODO: create database file,
    # assert that file does not exist
    # if forced create: overwrite=True
    try:
        c = conn.cursor()
        c.execute(query_create_question_table)
        c.execute(query_create_answer_vcs_table)
        c.execute(query_create_answer_table)
        c.execute(query_create_question_vcs_table)
        c.executescript(query_create_head_table)
        conn.commit()
        return 0
    except Error as e:
        print(e)
        return -1

    # TODO: put writing code into buffer and execute them all together


class DataBase:
    @staticmethod
    def init_database(
        db_file: str
    ):
        conn = None
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
            init_database_tables(conn)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()

    def __init__(
        self,
        db_file: str
    ):
        self.db_file = db_file
        # self.conn: sqlite3.Connection = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        # self.cursor =
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.conn.close()

    def get_git_head(self) -> str:
        c = self.conn.cursor()
        result = c.execute("""
        SELECT sha
        FROM GitHead
        """)
        l = list(result)
        return l[0][0]

    def update_git_head(self, sha: str, to_commit=False):
        c = self.conn.cursor()
        if is_empty(c, "GitHead"):
            c.execute(f"""
            INSERT INTO GitHead
            (id, sha)
            VALUES (0,'{sha}')
            """)
        else:
            c.execute(f"""
            UPDATE GitHead
            SET sha = '{sha}'
            WHERE id==0
            """)
        if to_commit:
            self.conn.commit()

    def has_answer(self, answer_id: str) -> bool:
        c = self.conn.cursor()
        return not is_empty(
            c, title_4_answer_table,
            condition=f"WHERE id=={answer_id}"
        )

    def has_question(self, question_id: str) -> bool:
        c = self.conn.cursor()
        return not is_empty(
            c, title_4_question_table,
            condition=f"WHERE id=={question_id}"
        )

    def _date2str(self, d: datetime.datetime) -> str:
        # FIXME
        return str(d)

    def add_answer(
        self, answer_id: int,
        dateCreated: datetime.datetime,
        question_id: int, author_id="NULL",  # FIXME
        to_commit=False
    ):
        c = self.conn.cursor()
        dateCreated_s = self._date2str(dateCreated)
        c.executescript(f"""
        INSERT INTO {title_4_answer_table}
        (id, authorId, questionId, dateCreated)
        VALUES
        ({answer_id}, {author_id},
        {question_id}, '{dateCreated_s}')
        """)
        if to_commit:
            self.conn.commit()

    def add_question(
        self,
        dateCreated: datetime.datetime,
        question_id: int,
        author_id="NULL",  # FIXME
        to_commit=False
    ):
        c = self.conn.cursor()
        dateCreated_s = self._date2str(dateCreated)
        c.executescript(f"""
        INSERT INTO {title_4_question_table}
        (id, authorId, dateCreated)
        VALUES ({question_id}, {author_id}, '{dateCreated_s}')
        """)
        if to_commit:
            self.conn.commit()

    def add_answer_version(
        self,
        answer_id: int, commit_id: str,
        dateFetched: datetime.datetime,
        dateModified: datetime.datetime,
        commentCount: int,
        to_commit=False
    ):
        #  dateFetched, dateModified,
        c = self.conn.cursor()
        dateFetched_s = self._date2str(dateFetched)
        dateModified_s = self._date2str(dateModified)
        c.executescript(f"""
        INSERT INTO {title_4_answer_table}VCS
        (commitId, answerId,
        dateFetched, dateModified,
        commentCount)
        VALUES
        ('{commit_id}',{answer_id},
        '{dateFetched_s}','{dateModified_s}',
        {commentCount})""")
        if to_commit:
            self.conn.commit()

    def add_question_version(
        self,
        question_id: int, commit_id: str,
        dateFetched: datetime.datetime,
        dateModified: datetime.datetime,
        answerCount: int,
        to_commit=False
    ):
        c = self.conn.cursor()
        dateFetched_s = self._date2str(dateFetched)
        dateModified_s = self._date2str(dateModified)
        c.executescript(f"""
        INSERT INTO {title_4_question_table}VCS
        (commitId, questionId,
        dateFetched, dateModified,
        answerCount)
        VALUES
        ('{commit_id}', {question_id},
        '{dateFetched_s}', '{dateModified_s}',
        {answerCount})""")
        if to_commit:
            self.conn.commit()

    def commit(self):
        self.conn.commit()
