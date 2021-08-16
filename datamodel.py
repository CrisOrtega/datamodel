import config
from debug import Debug
import sqlparser

import os
import sys
import re
import json

def all_sql_files(path):
    ### This returns the list of files in a specific folder
    list_of_files=[]
    if not os.path.exists(path):
        raise ValueError("PATH: {} not existing".format(path))

    for root, dirs, files in os.walk(path):
        for f in files:
            filename=r'^(.+)\.(\w+)$'
            result=re.search(filename,f)
            # result contains the result of the search
            # this changed after python 3.6 and now it is not possible to reference result like result[2]
            # now I need to use the method group
            # result will be a _sre.SRE_Match object
            # result.group(0) will be the full name of the file
            # result.group(1) will be the name of the file
            # result.group(2) will be the extension of the file
            # What I'm checking here is that the extension is one of the considered extensions
            if result != None and result.group(2) in config.sql_extensions:
                list_of_files.append(os.path.join(root,f))
    return list_of_files

def removeComments(string):
    try:
        # remove all occurrences streamed comments (/*COMMENT */) from string
        string = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,';' ,string)
        string = re.sub(re.compile("//.*?\n" ) ,' ' ,string)
        string = re.sub(re.compile("--.*?\n"), ' ', string)
        string = re.sub(re.compile("^#.*?\n"), ' ', string)
        # remove all occurrence single-line comments (//--#COMMENT\n ) from string
        return string
    except IOError as e:
        return ""

def process_file(file):
    queries=[]
    lines_to_process=process_file_extractlines(file)
    for line in lines_to_process:
        if line.strip() != '':
            queries.append(line.strip())
    return queries

def process_file_extractlines(file):
    queries=[]
    sql_file = open(file, 'r', encoding='utf-8')
    file_content = sql_file.read()
    # For the sake of simplicity I'm going to assume all sql is split by comments or ;
    queries = removeComments(file_content)
    # First I extract it into a single line
    queries=" ".join(queries.split())
    # Second I split the line by ;
    queries=queries.split(";")
    return queries


def analyze(tables,fields):
    output={}
    for table,alias in tables.items():
        if table not in output.keys():
            output[table]=[]
        for field in fields:
            if field[0]==alias[0] and field[1] not in output[table] and (field[0]!='' or len(tables)==1):
                output[table].append(field[1])
            if field[0]==table and field[1] not in output[table]:
                output[table].append(field[1])
    return output


def process_all_files(list_of_files):
    whole_tables = {}
    for f in list_of_files:
        queries = process_file(f)
        for query in queries:
            dbg.msg('process', 'file', 'sql file', 1, f)
            dbg.msg('process', 'query', 'query', 1, query[:50])
            # query = "Select a.col1, b.col2 from tb1 as a inner join tb2 as b on tb1.col7 = tb2.col8;"
            # info=sqlparser.mylex(query.lower())
            tables = sqlparser.find_all_tables(query)
            dbg.msg('process', 'query', 'tables', 1, str(tables).replace("[", "/").replace("]", "/"))
            fields = sqlparser.find_all_fields(query)
            dbg.msg('process', 'query', 'fields', 1, str(fields).replace("[", "/").replace("]", "/"))
            last_tables = analyze(tables, fields)
            for table, fields in last_tables.items():
                if table not in whole_tables.keys():
                    whole_tables[table] = [[], []]
                    whole_tables[table][0] = fields
                    whole_tables[table][1].append(f)
                else:
                    in_whole_tables = set(whole_tables[table][0])
                    in_fields = set(fields)
                    in_fields_not_in_whole = in_fields - in_whole_tables
                    whole_tables[table][0] = whole_tables[table][0] + list(in_fields_not_in_whole)
                    if f not in whole_tables[table][1]:
                        whole_tables[table][1].append(f)
    dbg.msg('process', 'whole tables', 'tables', 1, str(whole_tables)[:100].replace("[", "/").replace("]", "/"))
    return whole_tables

def process_whole_tables(whole_tables):
    dict_to_json=[]
    for table in whole_tables:
        whole_tables[table][0].sort()
        whole_tables[table][1].sort()
        dict = {'table':table,'fields':whole_tables[table][0],'files':whole_tables[table][1]}
        dict_to_json.append(dict)
    with open(config.sql_model, "w") as outfile:
        json.dump(dict_to_json, outfile,indent=4)
        dbg.msg('write','file','json',2,'Printint Datamodel to {}'.format(config.sql_model))


def main():
    # We first extract all files in the path that have an extension in config.sql_extensions
    list_of_files = all_sql_files(config.sql_path)
    # Now we process all files
    whole_tables=process_all_files(list_of_files)
    process_whole_tables(whole_tables)
    

    # TODO Luego es necesario procesar whole_tables, y crear, tablespace,table, listacampos
    # TODO Sacarlo tdo a un fichero de configuracion
    # TODO A partir de ahi es pintar las entidades sueltas
    # TODO pintar las relaciones entre tablas





if __name__ == "__main__":
    # Initialize debuger
    dbg = Debug(os.path.basename(__file__), level=2)
    dbg.msg('Version', 'sys.version', 'sys.version', 1, sys.version)
    dbg.msg('config', 'path', 'sql path', 1, config.sql_path)
    main()