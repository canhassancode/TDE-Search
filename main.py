#   ______          _____ _______ 
# |  ____|/\      / ____|__   __|
# | |__  /  \    | (___    | |   
# |  __|/ /\ \    \___ \   | |   
# | |_ / ____ \ _ ____) |  | |   
# |_(_)_/    \_(_)_____(_) |_|   
# 
# Author: Hassan (hassan.4.ali@bt.com)
# Version: 1.1                                 


###########################################
# IMPORTED MODULES
###########################################

import yaml
import os
import pandas as pd

###########################################
# VARIABLES
###########################################

yaml_list = []


###########################################
# MAIN CODE
###########################################

# Find all YML files by walking through all directories
def yaml_files(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".yml"):
                current_yaml = (os.path.join(root, file)).replace("\\", "/")
                yaml_list.append(current_yaml)

def find_tag(path, input_tag):
    yaml_files(path)  # obtain all the yaml files available
    counter = 0
    error_counter = 0
    output_list = []

    for yaml_file in yaml_list:
        try:
            # stream = open(yaml_file, "r", encoding="utf-8")
            stream = open(yaml_file, "r")
            temp_yaml = yaml.safe_load(stream)
            for tag in temp_yaml['tags']:
                if tag == "attack." + input_tag:
                    counter += 1
                    output_list.append(yaml_file)
                    print(counter, ". ",yaml_file)
        except yaml.YAMLError as x:
            # print("YAML ERROR: ", x)
            stream = open(yaml_file, "r")
            temp_yaml = list(yaml.safe_load_all(stream))
            for tag in temp_yaml[0]['tags']:
                if tag == "attack." + input_tag:
                    counter += 1
                    output_list.append(yaml_file)
                    print(counter, ". ",yaml_file)
            continue
        except KeyError as y:
            # print("KEY ERROR: ", y)
            error_counter+=1
            continue
        except UnicodeDecodeError as z:
            # print("UNICODE ERROR: ", z, yaml_file)
            error_counter+=1
            continue
    
    print("Number of files found: ", counter)  # final output


###########################################
# RUN CODE
###########################################
def main_code():
    print("############### Output for TDE Search ###############")
    print("")

    # Directory of folder and user input
    print("Input directory of the RULES folder e.g. (C:/Users/XXXX/Documents/tde/rules)")

    path = input("type here: ")
    input_tag = input("attack tag (e.g. t1047): ")

    find_tag(path, input_tag)

    print("To run another query type y")
    print("To close windows press any other key")

    k = input("Input here: ")
    try:
        if k == "y":
            main_code()
        else:
            print("Thank you")
    except Exception:
        print("Thank you")


main_code()


