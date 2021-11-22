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


# Opening YAML/YML files and search for attack.t tag
def find_tag():
    yaml_files()  # obtain all the yaml files available
    counter = 0
    output_list = []
    for yaml_file in yaml_list:
        with open(yaml_file, "r") as stream:
            try:
                # load the yaml file into a temp variable
                temp_yaml = yaml.safe_load(stream)
                # print(temp_yaml)
                for tag in temp_yaml['tags']:
                    if tag == "attack." + input_tag:
                        counter += 1
                        output_list.append(yaml_file)
                        print(counter, ". ",yaml_file)

            except (yaml.YAMLError, KeyError, UnicodeDecodeError) as e:
                continue
                print(e)
    
    print("Number of files found: ", counter)  # final output


###########################################
# RUN CODE
###########################################
print("############### Output for TDE Search ###############")
print("")
find_tag()

input("press enter to close window...")
