import re
from datetime import datetime

def find_all_tables_and_fields(string):
    tables={}
    fields = find_all_fields(string)

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
    noalias.append(r"from\s+(\w+\.\w+)\s?$")
    noalias.append(r"from\s+(\w+\.\w+)\s+")
    noalias.append(r"from\s+(\w+)\s+where")
    noalias.append(r"from\s+(\w+)\s+group")
    noalias.append(r"from\s+(\w+)\s+order")
    noalias.append(r"\s+join\s+(\w+\.\w+)\s+on\s+")
    noalias.append(r"\s+join\s+(\w+)\s+on\s+")

    # This is in case that there is a subquery and this subquery does not have any "(" or ")" inside
    specialcase=[]
    specialcase.append(r"from\s+\(([^)]+)\)\s+as\s+\w+")
    specialcase.append(r"join\s+\(([^)]+)\)\s+as\s+\w+")

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

    i=0
    for special in specialcase:
        result = re.findall(special, string)
        if result != None:
            for res in result:
                new_tables,new_fields=find_all_tables_and_fields(res)
                now = datetime.now()
                variable = now.strftime('%H%M%S')+str(i)
                i+=1
                for new_table in new_tables:
                    if new_table not in tables.keys():
                        tables[new_table]=[]
                        tables[new_table].append(variable)
                for new_field in new_fields:
                    if new_field[0] == '':
                        fields.append([variable,new_field[1]])
                    else:
                        fields.append(new_field)

    return tables,fields

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
    # de select a from un campo
    lpattern_select_fields.append(r"select\s+\s?(\w+)\s?\s+from")
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
    # All select fields, without ., functions broke it
    #lpattern_select_fields.append(r"(?:SELECT\s++(?=(?:[#\w,`.]++\s++)+)|(?!^)\G\s*+,\s*+(?:`?+\s*+[#\w]++\s*+`?+\s*+\.\s*+)?+`?+\s*+)(\w++)`?+(?:\s++as\s++[^,\s]++)?+")
    #preg_match_all('/(?:SELECT\s++(?=(?:[\#\w,`.]++\s++)+) # start matching on SELECT
    #               |  # or
    #               (?! ^)\G  # resume from last match position
    #\s * +,\s * +  # delimited by a comma
    #(?:`?+\s * +  # optional prefix table with optional backtick
    #[\  # \w]++   # table name
    #\s * +`?+  # optional backtick
    #\s * +\.\s * +  # dot separator
    #)?+  # optional prefix table end group
    #`?+\s * +  # optional backtick
    #)  # initial match or subsequent match
    #(\w++)  # capturing group
    #`?+  # optional backtick

    for pattern in lpattern_select_fields:
        result = re.findall(pattern, string)
        for res in result:
            fields.append(['',res])

    return fields