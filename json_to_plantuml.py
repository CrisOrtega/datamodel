import config
from debug import Debug

import json
import os
import sys
import re
from datetime import datetime

def readjson(jsonfile):
    with open(jsonfile) as json_file:
        data = json.load(json_file)
    return data

def writeheaders(datamodel):
    headers=[]
    headers.append("""@startuml
' uncomment the line below if you're using computer with a retina display
' skinparam dpi 300
!define Table(name,desc) class name as "desc" << (T,#FFAAAA) >>
' we use bold for primary key
' green color for unique
' and underscore for not_null
!define primary_key(x) <b>x</b>
!define unique(x) <color:green>x</color>
!define not_null(x) <u>x</u>
' other tags available:
' <i></i>
' <back:COLOR></color>, where color is a color name or html color code
' (#FFAACC)
' see: http://plantuml.com/classes.html#More
hide methods
hide stereotypes

' entities""")
    return headers

def writemodel(datamodel):
    model=[]
    for table_row in datamodel:
        if "." in table_row['table']:
            type="Table"
            model.append("{}({},\"{}\"){{".format(type, table_row['table'], table_row['table']))
        else:
            type='Object'
            model.append("{} {} {{".format(type, table_row['table']))


        for field in table_row['fields']:
            model.append("{}".format(field))
        model.append('}\n\n')
    return model

def writerelations(relations):
    relat=[]
    relat.append("""' relationships
' one-to-one relationship
' user -- user_profile : "A user only has one profile"
' one to may relationship
' user --> session : "A user may have many sessions"
' many to many relationship
' Add mark if you like""")
    relat.append("'examples")
    relat.append("""' user "1" --> "*" user_group : "A user may be in many groups"
' group "1" --> "0..N" user_group : "A group may contain many users"
""")
    relat.extend(relations)
    return relat

def closefile(datamodel):
    close=[]
    close.append("""@enduml""")
    return close

def writeplantuml(file):
    pattern = r".+\[(.+)\].+"
    datefileformat = re.search(pattern, config.plant_uml)[1]
    now = datetime.now()
    try:
        dt_string = now.strftime(datefileformat)
    except IOError as e:
        raise ValueError("Bad date format in name: {} ".format(datefileformat))
    pattern = r"\[.+\]"
    plantuml_file_name = re.sub(pattern, dt_string, config.plant_uml)
    with open(plantuml_file_name, 'w') as f:
        for item in file:
            f.write("%s\n" % item)

def process_relations(datamodel):
    relations = []
    for table_row in datamodel:
        for item in table_row['relations']:
            rep=item.split(' -> ')
            reptable=rep[1]
            pre2=reptable.split('.')
            pre1=table_row['table'].split('.')
            if len(pre1)>1 and len(pre2)>1 and pre1[0]==pre2[0]:
                item1=table_row['table']
                item2=reptable
            else:
                item1 = pre1[0]
                item2 = pre2[0]

            if item1 <= item2:
                relation="{} \"*\" --> \"*\" {}".format(item1,item2)
            else:
                relation = "{} \"*\" --> \"*\" {}".format(item2,item1)
            if relation not in relations:
                relations.append(relation)
    relations.sort()
    return relations

def main():
    # We read the json
    datamodel = readjson(config.json_sql_model_fixed)
    dbg.msg('read','file','json',1,str(datamodel)[:100])

    # we create the file variable
    file = []

    # we append the headers
    file.extend(writeheaders(datamodel))

    # we write the data model
    file.extend(writemodel(datamodel))

    # we extract and process relations
    relations=process_relations(datamodel)
    file.extend(writerelations(relations))

    #we end the file
    file.extend(closefile(datamodel))

    #we write the file
    writeplantuml(file)

if __name__ == "__main__":
    # Initialize debuger
    dbg = Debug(os.path.basename(__file__), level=1)
    dbg.msg('Version', 'sys.version', 'sys.version', 1, sys.version)
    main()
    # Use
    # https://plantuml-editor.kkeisuke.com/
    # to visualize
    # TODO abrir branch nuevo
    # TODO make two outputs with and without relations
    # TODO black list for relationships
