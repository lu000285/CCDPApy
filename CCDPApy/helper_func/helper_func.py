import pandas as pd
import numpy as np
import os, re
from pathlib import Path

###########################################################################
def get_unit(string):
    pattern = r"\((.*?)\)"  # Matches the content within parentheses. E.g. (mL)

    match = re.search(pattern, string)
    if match:
        content_within_parentheses = match.group(1)
        # Remove parentheses and their contents from the original string
        # string_without_parentheses = re.sub(pattern, "", string).strip()
    else:
        content_within_parentheses = ''
        # string_without_parentheses = string

    return content_within_parentheses

def split_name_unit(string):
    '''Split the string into the parameter name and its unit using regular expression.
    '''
    pattern = r"(\(.*\))"
    match = re.search(pattern, string)
    if match:
        splits = re.split(pattern, string)
        return splits[0][:-1], splits[1]
    else:
        return string, ''

###########################################################################
# Check Error for Pandas
def check_key(df, key):
    try:
        return (df[key])
    except Exception as e:
        # print(f'Error {e}')
        return pd.Series(data=np.nan)
###########################################################################

###########################################################################
# Check Input File Path
def input_path(file_name):
    # Base directry where this file exits
    BASE_DIR = Path(__file__).resolve().parent

    # Input directry path
    INPUT_BASE = os.path.join(BASE_DIR.parent.parent, 'input_files')

    # Input file path
    INPUT_FILE_PATH = os.path.join(INPUT_BASE, file_name)
    
    return INPUT_FILE_PATH
###########################################################################

###########################################################################
# Check Output File Path
def output_path(file_name):
    # Base directry where this file exits
    BASE_DIR = Path(__file__).resolve().parent

    # Input directry path
    OUTPUT_BASE = os.path.join(BASE_DIR.parent.parent, 'output_files')

    # Make output files directry
    try:
        os.makedirs(OUTPUT_BASE)    
        print("Directory " , OUTPUT_BASE ,  " Created ")
    except FileExistsError:
        pass
        # print("Directory " , OUTPUT_BASE ,  " already exists")

    # Input file path
    OUTPUT_FILE_PATH = os.path.join(OUTPUT_BASE, file_name)
    
    return OUTPUT_FILE_PATH