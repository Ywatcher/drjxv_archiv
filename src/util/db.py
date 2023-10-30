# -*- coding: utf-8 -*-

def is_empty(cursor, table: str, condition: str = '') -> bool:
    # condition: empty or begin with "WHERE"
    result = cursor.execute(
        f"SELECT EXISTS (SELECT 1 FROM {table} {condition});")
    l = list(result)
    return l[0][0] == 0
