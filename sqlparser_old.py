# This is no my sql parser but it has been taken from stack overflow
# https://stackoverflow.com/questions/35624662/how-to-extract-table-names-and-column-names-from-sql-query

import ply.lex as lex, re
import re

def find_all_tables(string):
    pattern_from=r"from\s+(\w+\.\w+)\s+as\s+(\w+)"
    pattern_from2 = r"from\s+(\w+\.\w+)\s+"
    pattern_join=r"\s+join\s+(\w+)\s+as\s+(\w+)"
    result=re.findall(pattern_from,string)
    print(result)
    result = re.findall(pattern_from, string)
    print(result)
    result2=re.findall(pattern_join,string)
    result(result2)




tokens = (
    "TABLE",
    "JOIN",
    "COLUMN",
    "GROUPING",
    "VALUE",
    "COLUMN_NOTABLE",
    "TRASH",
    "TRASH2",
    "TRASH3",
    "TRASHZ"

)

tables = {"tables": {}, "alias": {}}
columns = []

#COA: I lower() the select
t_TRASH = r"select|on|=|;|\s+|,|\t|\r|where"
t_TRASH2=r"is\s+not\s+null"
t_TRASH3=r"group\s+by\s+[0-9]?"
t_TRASHZ=r"order\s+by\s+"

def t_TABLE(t):
    r"from\s(.+)\sas\s(\w+)"

    regex = re.compile(t_TABLE.__doc__)
    m = regex.search(t.value)
    if m is not None:
        tbl = m.group(1)
        alias = m.group(2)
        tables["tables"][tbl] = ""
        tables["alias"][alias] = tbl

    return t

def t_JOIN(t):
    r"inner\s+join\s+(\w+)\s+as\s+(\w+)"

    regex = re.compile(t_JOIN.__doc__)
    m = regex.search(t.value)
    if m is not None:
        tbl = m.group(1)
        alias = m.group(2)
        tables["tables"][tbl] = ""
        tables["alias"][alias] = tbl
    return t

def t_COLUMN(t):
    r"(\w+\.\w+)"

    regex = re.compile(t_COLUMN.__doc__)
    m = regex.search(t.value)
    if m is not None:
        t.value = m.group(1)
        columns.append(t.value)
    return t

def t_GROUPING(t):
    r"(count|max|sum|min)?\((distinct|)?\s?(.+)\s?\)"

    regex = re.compile(t_GROUPING.__doc__)
    m = regex.search(t.value)
    if m is not None:
        t.value = m.group(3)
        columns.append(t.value)
    return t
def t_VALUE(t):
    r"(.+)\s?=.+(and|or)"

    regex = re.compile(t_GROUPING.__doc__)
    m = regex.search(t.value)
    if m is not None:
        t.value = m.group(1)
        columns.append(t.value)
    return t

def t_COLUMN_NOTABLE(t):
    r"(\w+)\s?(,|from)"

    regex = re.compile(t_COLUMN_NOTABLE.__doc__)
    m = regex.search(t.value)
    if m is not None:
        t.value = m.group(1)
        #columns.append(t.value)
        print("Column {} is lost".format(t.value))
    return t

def t_error(t):
    print(columns)
    raise TypeError("Unknown text '%s'" % (t.value,))
    t.lexer.skip(len(t.value))

# here is where the magic starts
def mylex(inp):
    lexer = lex.lex()
    lexer.input(inp)

    for token in lexer:
        pass

    result = {}
    print(columns)
    for col in columns:
        tbl, c = col.split('.')
        if tbl in tables["alias"].keys():
            key = tables["alias"][tbl]
        else:
            key = tbl

        if key in result:
            result[key].append(c)
        else:
            result[key] = list()
            result[key].append(c)

    return result
    # {'tb1': ['col1', 'col7'], 'tb2': ['col2', 'col8']}

