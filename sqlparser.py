import re

def find_all_tables(string):
    tables={}
    # results with alias
    alias=[]
    alias.append(r"from\s+(\w+\.\w+)\s+as\s+(\w+)")
    alias.append(r"from\s+(\w+)\s+as\s+(\w+)")
    alias.append(r"from\s+(\w+\.\w+)\s+(\w+)\s+where\s+")
    alias.append(r"from\s+(\w+\.\w+)\s+(\w+)\s+where\s+")
    alias.append(r"from\s+(\w+\.\w+)\s+(\w+)\s+left\s+")
    alias.append(r"from\s+(\w+)\s+(\w+)\s+left\s+")
    alias.append(r"from\s+(\w+\.\w+)\s+(\w+)\s+right\s+")
    alias.append(r"from\s+(\w+)\s+(\w+)\s+right\s+")
    alias.append(r"from\s+(\w+\.\w+)\s+(\w+)\s+inner\s+")
    alias.append(r"from\s+(\w+)\s+(\w+)\s+inner\s+")
    alias.append(r"\s+join\s+(\w+\.\w+)\s+as\s+(\w+)")
    alias.append(r"\s+join\s+(\w+)\s+as\s+(\w+)")
    alias.append(r"\s+join\s+(\w+\.\w+)\s+(\w+)\s+on")
    alias.append(r"\s+join\s+(\w+)\s+(\w+)\s+on")


    # results without alias
    noalias=[]
    noalias.append(r"from\s+(\w+\.\w+)\s+")
    noalias.append(r"from\s+(\w+)\s+where")
    noalias.append(r"from\s+(\w+)\s+group")
    noalias.append(r"from\s+(\w+)\s+order")
    noalias.append(r"\s+join\s+(\w+\.\w+)\s+on\s+")
    noalias.append(r"\s+join\s+(\w+)\s+on\s+")


    for alia in alias:
        result = re.findall(alia, string)
        if result != None:
            for res in result:
                if res[0] not in tables.keys():
                    tables[res[0]]=[]
                    tables[res[0]].append(res[1])
                else:
                    if res[1] not in tables[res[0]]:
                        tables[res[0]].append(res[1])

    for alia in noalias:
        result = re.findall(alia, string)
        if result != None:
            for res in result:
                if res not in tables.keys():
                    tables[res]=['']

    return tables

def find_all_fields(string):
    fields=[]
    fpattern_select_fields=[]
    fpattern_select_fields.append(r"select(.+)from\s+")
    fpattern_select_fields.append(r"\s+on\s+(.+)\s+where\s+")
    fpattern_select_fields.append(r"\s+on\s+(.+)\s+and\s+")
    fpattern_select_fields.append(r"\s+where\s+(.+)\s+group\s+")
    fpattern_select_fields.append(r"\s+where\s+(.+)\s+order\s+")
    for pattern_select_fields in fpattern_select_fields:
        result = re.findall(pattern_select_fields, string)
        if result != None:
            for res in result:
                pattern=r'(\w+)\.(\w+)'
                result_int=re.findall(pattern, res)
                fields.extend(result_int)

    #Hay que descartar las que sean numeros
    lpattern_select_fields=[]
    # de select a from entre comas
    lpattern_select_fields.append(r"select\s+.+,\s?(\w+)\s?,.+\s+from")
    # despues de select
    lpattern_select_fields.append(r"select\s+(\w+)\s?,.+\s+from")
    # antes de from
    lpattern_select_fields.append(r"select\s+.+,\s?(\w+)\s+from")
    # ente parentesis
    lpattern_select_fields.append(r"select\s+.+\(\s?(\w+)\s?\).+\s+from")
    # Entre parentesis con distinct
    lpattern_select_fields.append(r"select\s+.+\(\s?distinct\s+(\w+)\s?\).+\s+from")
    # substring y similares
    lpattern_select_fields.append(r"select\s+.+\(\s?(\w+)\s?,.+\).+\s+from")

    for pattern in lpattern_select_fields:
        result = re.findall(pattern, string)
        for res in result:
            fields.append(['',res])

    return fields