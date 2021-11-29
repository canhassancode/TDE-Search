print("  ______          _____ _______") 
print("|  ____|/\      / ____|__   __|")
print("| |__  /  \    | (___    | |")   
print("|  __|/ /\ \    \___ \   | |")   
print("| |_ / ____ \ _ ____) |  | |")   
print("|_(_)_/    \_(_)_____(_) |_|")   
print("") 
print("# Author: Hassan (hassan.4.ali@bt.com")
print("# Version: 1.1")          
print("")                       


###########################################
# IMPORTED MODULES
###########################################

from pandas.core.groupby.generic import AggScalar
import yaml
import os
import pandas as pd

###########################################
# VARIABLES
###########################################

yaml_list = []
df = ""
data = {
    'IDs': [],
    'Location': [],
    'Number of Files': []
}

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
    location_string = ""
    # data["IDs"][input_tag] = []
    # data["IDs"]["IDs"] = input_tag

    data["IDs"].append(input_tag)

    for yaml_file in yaml_list:
        try:
            stream = open(yaml_file, "r", encoding="utf-8")
            # stream = open(yaml_file, "r")
            temp_yaml = yaml.safe_load(stream)
            for tag in temp_yaml['tags']:
                if tag == "attack." + input_tag:
                    counter += 1
                    output_list.append(yaml_file)
                    print(counter, ". ",yaml_file)
                    # data["IDs"].append(input_tag)
                    # data["Location"].append(yaml_file)
                    # data["IDs"][input_tag].append(yaml_file)
                    location_string = (yaml_file.split("rules")[1] + ', ' + location_string)
        except yaml.YAMLError as x:
            # print("YAML ERROR: ", x)
            stream = open(yaml_file, "r")
            temp_yaml = list(yaml.safe_load_all(stream))
            for tag in temp_yaml[0]['tags']:
                if tag == "attack." + input_tag:
                    counter += 1
                    output_list.append(yaml_file)
                    print(counter, ". ",yaml_file)
                    # data["IDs"].append(input_tag)
                    # data["Location"].append(yaml_file)
                    # data["IDs"][input_tag].append(yaml_file)
                    location_string = (yaml_file.split("rules")[1] + ', ' + location_string)
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
    data["Location"].append(location_string)
    data["Number of Files"].append(counter)
    global df
    df = pd.DataFrame(data)

# Manual input option
def manual_opt():
    print("############### Manual output for TDE Search ###############")
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
            manual_opt()
        else:
            print("(IMPORTANT)Please specify Folder for output excel file e.g. (C:/Users/XXXX/Documents/output.xlsx)")
            output_name = input("Input here: ")
            try: 
                df.to_excel(output_name, index=False, header=True)
                print("Success!")
            except Exception as e:
                print(e)
    except Exception:
        print("Thank you")
    

def auto_opt():
    print("############### Automated excel output for TDE Search ###############")
    print("")

    # Directory of folder and user input
    print("Input directory of the RULES folder e.g. (C:/Users/XXXX/Documents/tde/rules)")
    path = input("type here: ")
    print("")

    # Location of Excel file
    print("Input excel file directory e.g. (C://Users/XXXX/Documents/spreadsheet.xlsx)")
    input_tag = input("type here: ")

    input_file = pd.read_excel(input_tag, engine='openpyxl')
    col = input_file.columns[0]
    tags = input_file[col].tolist()
    print(tags)

    for tag in tags:
        find_tag(path, tag)

    print("To run another query type y")
    print("To close windows press any other key")
    
    k = input("Input here: ")
    try:
        if k == "y":
            manual_opt()
        else:
            print("(IMPORTANT)Please specify Folder for output excel file e.g. (C:/Users/XXXX/Documents/output.xlsx)")
            output_name = input("Input here: ")
            try: 
                df.to_excel(output_name, index=False, header=True)
                print("Success!")
            except Exception as e:
                print(e)
    except Exception:
        print("Thank you")

###########################################
# RUN CODE - MAIN LOOP
###########################################
def main_code():
    print("Enter 1 for manual. Enter 2 for automated excel input")
    input_opt = input("1 or 2: ")

    if input_opt == "1":
        manual_opt()
    elif input_opt == "2":
        auto_opt()
    


main_code()


