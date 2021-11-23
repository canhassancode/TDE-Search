###########################################
# IMPORTED MODULES
###########################################

import yaml
import os

###########################################
# VARIABLES
###########################################

yaml_list = []
input_tag = ""

###########################################
# MAIN CODE
###########################################

# Directory of folder and user input
print("Input directory of the RULES folder e.g. (C:/Users/XXXX/Documents/tde/rules)")

path = input("type here: ")
input_tag = input("attack tag (e.g. t1047): ")


# Find all YML files by walking through all directories
def yaml_files():
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".yml"):
                current_yaml = (os.path.join(root, file)).replace("\\", "/")
                yaml_list.append(current_yaml)

def find_tag():
    yaml_files()  # obtain all the yaml files available
    counter = 0
    error_counter = 0
    output_list = []

    for yaml_file in yaml_list:
        try:
            stream = open(yaml_file, "r", encoding="utf-8")
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
            print("KEY ERROR: ", y)
            error_counter+=1
            continue
        except UnicodeDecodeError as z:
            print("UNICODE ERROR: ", z, yaml_file)
            error_counter+=1
            continue
    
    print("Number of files found: ", counter)  # final output

###########################################
# RUN CODE
###########################################
print("############### Output for TDE Search ###############")
print("")
find_tag()

input("press enter to close window...")