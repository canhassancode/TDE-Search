print(" ______          _____ _______") 
print("|  ____|/\      / ____|__   __|")
print("| |__  /  \    | (___    | |")   
print("|  __|/ /\ \    \___ \   | |")   
print("| |_ / ____ \ _ ____) |  | |")   
print("|_(_)_/    \_(_)_____(_) |_|")   
print("") 
print("# Author: Hassan (hassan.4.ali@bt.com)")
print("# Version: 1.4")          
print("")                       

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
    logsource = ["product", "service"]

    for yaml_file in yaml_list:
        try:
            stream = open(yaml_file, "r", encoding="utf-8")
            temp_yaml = yaml.safe_load(stream)
            for tag in temp_yaml['tags']:
                if tag == "attack." + input_tag:
                    counter += 1
                    print(counter, ". ",yaml_file)
                    location_string = yaml_file.split("rules")[1]

                    # ADDITIONAL PARAMETERS

                    # Logsource
                    if "1" in add_opt:

                        # Product
                        try:
                            product = str(temp_yaml["logsource"]["product"])
                            data["Product"].append(product)
                        except Exception:
                            data["Product"].append("Nothing found.")

                        # Service
                        try:
                            service = str(temp_yaml["logsource"]["service"])
                            data["Service"].append(service)
                        except Exception:
                            data["Service"].append("Nothing found.")

                        # Other
                        try:
                            other_logsource = ""
                            for index in temp_yaml["logsource"]:
                                if index not in logsource:
                                    other_logsource += (str(index) + ": " + str(temp_yaml["logsource"][index]) + ", ")
                            other_logsource = other_logsource[:-1]
                            other_logsource = other_logsource[:-1]
                            if other_logsource == "":
                                other_logsource = "Nothing found."
                            data["Other"].append(other_logsource)
                        except Exception:
                            data["Other"].append("Nothing found.")
                    # ----------------    

                    data["IDs"].append(input_tag)
                    data["Location"].append(location_string)

        except yaml.YAMLError as x:
            stream = open(yaml_file, "r")
            temp_yaml = list(yaml.safe_load_all(stream))

            for sub_yaml in range(len(temp_yaml)):
                try:
                    for tag in temp_yaml[0]['tags']: # TODO: Add feature to go through sub-yamls regardless of later tags
                        if tag == "attack." + input_tag:
                            counter += 1
                            print(counter, ". ",yaml_file)
                            location_string = yaml_file.split("rules")[1]

                            # ADDITIONAL PARAMETERS

                            # Logsource -------
                            if "1" in add_opt:

                                # Product
                                try:
                                    product = str(temp_yaml["logsource"]["product"])
                                    data["Product"].append(product)
                                except Exception:
                                    data["Product"].append("Nothing found.")

                                # Service
                                try:
                                    service = str(temp_yaml["logsource"]["service"])
                                    data["Service"].append(service)
                                except Exception:
                                    data["Service"].append("Nothing found.")

                                # Other
                                try:
                                    other_logsource = ""
                                    for index in temp_yaml["logsource"]:
                                        if index not in logsource:
                                            other_logsource += (str(index) + ": " + str(temp_yaml["logsource"][index]) + ", ")
                                    other_logsource = other_logsource[:-1]
                                    other_logsource = other_logsource[:-1]
                                    if other_logsource == "":
                                        other_logsource = "Nothing found."
                                    data["Other"].append(other_logsource)
                                except Exception:
                                    data["Other"].append("Nothing found.")
                            # ----------------

                            data["IDs"].append(input_tag)
                            data["Location"].append(location_string)
                    continue
                except Exception as e:
                    # print("EXCEPTION KEY ERROR")
                    continue
        except KeyError as y:
            # print("KEY ERROR: ", yaml_file)
            continue
        except UnicodeDecodeError as z:
            # print("UNICODE ERROR: " + temp_yaml)
            continue
        except Exception as error:
            # print("ERROR: ", error)
            continue
    
    if counter == 0:
        data["IDs"].append(input_tag)
        data["Location"].append("No Rules associated")
        data["Product"].append("No Rules associated")
        data["Service"].append("No Rules associated")
        data["Other"].append("N/A")
    print("Number of rules found for", input_tag, ": ", counter)  # final output
    global df
    try:
        df = pd.DataFrame(data)
    except Exception as e:
        print(e)

# Manual input user 
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
    

# Automatic input from Excel file
def auto_opt(add_opt):
    print("############### Automated excel output for TDE Search ###############")
    print("")

    # Location of Excel file
    print("Input excel file directory e.g. (C://Users/XXXX/Documents/spreadsheet.xlsx)")
    input_tag = input("type here: ")

    input_file = pd.read_excel(input_tag, engine='openpyxl')
    col = input_file.columns[0]
    tags = input_file[col].tolist()

    for tag in tags:
        find_tag(tag.lower(), add_opt)

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
    input_modes = ["1", "2"]
    print("1) Manual Mode - Search by ID")
    print("2) Automated Mode - Search by Excel Sheet")
    print("3) Cleanup Mode - Housekeeping (coming soon...")
    input_opt = input("input here: ")
    while True:
        if input_opt not in input_modes:
            input_opt = input("ERROR. Please try again: ")
        else:
            break

    # Additional parameters
    add_modes = ["0", "1"]
    print("")
    print("IMPORTANT: All additional parameters include default!")
    print("For multiple paramters input multiple numbers. E.g. 123")
    print("0) Default mode - Output rules with relative locations")
    print("1) Logsources +")
    print("2) coming soon...")
    add_opt = input("input here: ")
    while True:
        if add_opt not in add_modes:
            add_opt = input("ERROR. Please try again: ")
        else:
            break

    if add_opt == "" or add_opt == "0":
        add_opt = "0"
    if "1" in add_opt:
        data["Product"] = []
        data["Service"] = []
        data["Other"] = []

    if input_opt == "1":
        manual_opt(add_opt)
    if input_opt == "2":
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
