print(" ______          _____ _______") 
print("|  ____|/\      / ____|__   __|")
print("| |__  /  \    | (___    | |")   
print("|  __|/ /\ \    \___ \   | |")   
print("| |_ / ____ \ _ ____) |  | |")   
print("|_(_)_/    \_(_)_____(_) |_|")   
print("") 
print("# Author: Hassan (hassan.4.ali@bt.com)")
print("# Version: 1.3")          
print("")                       

###########################################
# IMPORTED MODULES
###########################################

# from numpy import add
import yaml
import os
import pandas as pd

###########################################
# VARIABLES
###########################################

yaml_list = []
list_counter = 0
df = ""
data = {
    'IDs': [],
    'Location': []
}

###########################################
# MAIN CODE
###########################################

def find_tag(input_tag, add_opt):
    counter = 0
    error_counter = 0

    for yaml_file in yaml_list:
        try:
            stream = open(yaml_file, "r", encoding="utf-8")
            temp_yaml = yaml.safe_load(stream)
            for tag in temp_yaml['tags']:
                if tag == "attack." + input_tag:
                    counter += 1
                    print(counter, ". ",yaml_file)
                    location_string = yaml_file.split("rules")[1]
                    print("HERE", add_opt)

                    # Additonal parameters
                    if "1" in add_opt:
                        try:
                            logsource = str(temp_yaml["logsource"])
                            data["Logsource"].append(logsource)
                        except Exception as e:
                            input(e)
                            data["Logsource"].append("Error")
                    if "2" in add_opt:
                        try:
                            detection = str(temp_yaml["detection"])
                            data["Detection"].append(detection)
                        except Exception as f:
                            input(f)
                            data["Detection"].append(detection)
                    data["IDs"].append(input_tag)
                    data["Location"].append(location_string)

        except yaml.YAMLError as x:
            stream = open(yaml_file, "r")
            temp_yaml = list(yaml.safe_load_all(stream))
            for tag in temp_yaml[0]['tags']:
                if tag == "attack." + input_tag:
                    counter += 1
                    print(counter, ". ",yaml_file)
                    location_string = yaml_file.split("rules")[1]

                    # Additonal parameters
                    if "1" in add_opt:
                        try:
                            logsource = str(temp_yaml["logsource"])
                            data["Logsource"].append(logsource)
                        except Exception as e:
                            input(e)
                            data["Logsource"].append("Error")
                    if "2" in add_opt:
                        try:
                            detection = str(temp_yaml["detection"])
                            data["Detection"].append(detection)
                        except Exception as f:
                            input(f)
                            data["Detection"].append(detection)
            # input(x)
                    
            continue
        except KeyError as y:
            error_counter+=1
            input("KEY ERROR: ", temp_yaml)
            continue
        except UnicodeDecodeError as z:
            error_counter+=1
            input("UNICODE ERROR: ", temp_yaml)
            continue
        except Exception as error:
            input("Exception: ", temp_yaml)
            continue

    print("Number of rules found for", input_tag, ": ", counter)  # final output
    global df
    print(data)
    df = pd.DataFrame(data)

# Manual input option
def manual_opt(add_opt):
    print("############### Manual output for TDE Search ###############")
    print("")

    input_tag = input("attack tag (e.g. t1047): ")
    find_tag(input_tag.lower(), add_opt)

    print("To run another query type y")
    print("To close windows press any other key")
    
    k = input("Input here: ")
    try:
        if k == "y":
            manual_opt(add_opt)
        else:
            print("(IMPORTANT)Please specify Folder for output excel file e.g. (C:/Users/XXXX/Documents/output)")
            print("Do not specify extension of file e.g. xlsx or xls")
            output_name = input("Input here: ")
            try: 
                df.to_excel(output_name + '.xlsx', index=False, header=True)
                input("Success!")
            except Exception as e:
                input(e)
    except Exception:
        input("Thank you")
    

def auto_opt(add_opt):
    print("############### Automated excel output for TDE Search ###############")
    print("")

    # Location of Excel file
    print("Input excel file directory e.g. (C://Users/XXXX/Documents/spreadsheet.xlsx)")
    input_tag = input("type here: ")

    input_file = pd.read_excel(input_tag, engine='openpyxl')
    col = input_file.columns[0]
    tags = input_file[col].tolist()
    print(tags)

    for tag in tags:
        tag = tag.lower()
        find_tag(tag, add_opt)

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
                df.to_excel(output_name + '.xlsx', index=False, header=True)
                input("Success!")
            except Exception as e:
                input(e)
    except Exception as y:
        input(y)


###########################################
# RUN CODE - MAIN LOOP
###########################################
def main_code():
    # Initial options for Manual or Automated
    print("1) Manual Mode - Search by ID")
    print("2) Automated Mode - Search by Excel Sheet")
    input_opt = input("input here: ")

    # Additional parameters
    print("")
    print("IMPORTANT: All additional parameters include default!")
    print("For multiple paramters input multiple numbers. E.g. 123")
    print("0) Default mode - Output rules with relative locations")
    print("1) Logsources +")
    print("2) Detections (coming soon...)")
    add_opt = input("input here: ")

    if add_opt == "" or add_opt == "0":
        add_opt = "0"
    if "1" in add_opt:
        data["Logsource"] = []
    if "2" in add_opt:
        data["Detection"] = []

    if input_opt == "1":
        manual_opt(add_opt)
    elif input_opt == "2":
        auto_opt(add_opt)
    

# Find all files and append them to list for input
print("Input directory of the RULES folder e.g. (C:/Users/XXXX/Documents/tde/rules)")
path = input("type here: ")
print("")
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".yml"):
            current_yaml = (os.path.join(root, file)).replace("\\", "/")
            if current_yaml not in yaml_list:
                yaml_list.append(current_yaml)
                list_counter += 1
                print(list_counter, ". ", current_yaml)

print("")
print("Found ", list_counter, " rules in repository.")
main_code()
