# datamodel

## Description
The script review a folder tree, read all sql files and extract the queries

- datamodel.py
> read a folder tree, finds all sql and generates the json file with the model

- json_to_plantuml.py
> read the json file into a dictionary and creates the uml	

NOTE: The parser is not detecting all the cases, but it is a buch of cases to look. 
For a real sql interpreter that detect all fields and tables I would need much more time.
Maybe for the future.

## Dependencies
import os			#For file management
import sys 			#For system operations
import re			#For regex
import json 		#For the Database output file
import datetime 	#For date in file name

## Configuration
Configuration is in config file