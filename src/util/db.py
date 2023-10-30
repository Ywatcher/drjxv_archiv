# -*- coding: utf-8 -*-

def is_empty(cursor, table: str, condition: str = '') -> bool:
    """
    This function is to decide whether a table is empty with
    certain condition;
    :param cursor: the cursor of current connection to db
    :param table: name of table to check
    :param condition:  a string empty or begin with "WHERE"
    :return  whether the given table is empty, or whether there is no \
        records satisfying certain condition in given table.
    """
    # :param condition:
    result = cursor.execute(
        f"SELECT EXISTS (SELECT 1 FROM {table} {condition});")
    l = list(result)
    return l[0][0] == 0
