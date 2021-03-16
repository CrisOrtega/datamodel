# datamodel

## Description
The script review a folder tree, read all sql files and extract the queries

- datamodel.py
> read a folder tree, finds all sql and generates the json file with the model

- json_to_plantuml.py
> read the json file into a dictionary and creates the uml	

## Dependencies
import os	#For file management
import sys 	#For system operations
import re	#For regex
import json #For the Database output file

## Configuration
Configuration is in config file