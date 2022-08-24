import pandas as pd
import numpy as np
import os
from pathlib import Path

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