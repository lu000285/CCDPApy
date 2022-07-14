from operator import imod
import sys
import pandas as pd
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import math
import types
import os
from pathlib import Path

from test_package.my_class_test import CellLine
from test_package.my_func_test import bio_process

# Main Function
def main():
    # Base directry where this file exits
    BASE_DIR = Path(__file__).resolve().parent
    # Output directry path
    OUTPUT_BASE = os.path.join(BASE_DIR, 'output_files')
    # Make output files directry
    try:
        os.makedirs(OUTPUT_BASE)    
        print("Directory " , OUTPUT_BASE ,  " Created ")
    except FileExistsError:
        print("Directory " , OUTPUT_BASE ,  " already exists")

    aa = ['Lactate', 'Glucose', 'Glutamine', 'Asparagine', 'Aspartate']

    POLY_ORDER_FILE = 'polynomial_order.xlsx'
    POLY_ORDER_PATH = os.path.join(BASE_DIR, POLY_ORDER_FILE)

    INPUT_SHEET = 'Measured Data'
    INPUT_FILE1 = 'VS_NIIMBL VS-001.xlsx'     # File 1
    INPUT_FILE2 = 'VS_NIIMBL VS-002.xlsx'     # File 2
    INPUT_FILE3 = 'VS_NIIMBL VS-003.xlsx'     # File 3
    OUTPUT_FILE = 'Process.xlsx'

    IMG_FILE1 = 'CL1_1.png'
    IMG_FILE2 = 'CL1_2.png'
    IMG_FILE3 = 'CL1_3.png'

    OUTPUT = os.path.join(OUTPUT_BASE, OUTPUT_FILE)
    INPUT_1  = os.path.join(BASE_DIR, INPUT_FILE1)
    INPUT_2  = os.path.join(BASE_DIR, INPUT_FILE2)
    INPUT_3  = os.path.join(BASE_DIR, INPUT_FILE3)


    OUT_IMG1 = os.path.join(OUTPUT_BASE, IMG_FILE1)
    OUT_IMG2 = os.path.join(OUTPUT_BASE, IMG_FILE2)
    OUT_IMG3 = os.path.join(OUTPUT_BASE, IMG_FILE3)

    # Execute BioProcess
    bp1 = bio_process(input_file_name=INPUT_1,
                        measured_data_sheet_name=INPUT_SHEET,
                        aa_list=aa,
                        polyorder_file_name=POLY_ORDER_PATH)
    bp1.get_exp_info()

    bp2 = bio_process(input_file_name=INPUT_2,
                        measured_data_sheet_name=INPUT_SHEET,
                        aa_list=aa,
                        polyorder_file_name=POLY_ORDER_PATH)

    bp3 = bio_process(input_file_name=INPUT_3,
                        measured_data_sheet_name=INPUT_SHEET,
                        aa_list=aa,
                        polyorder_file_name=POLY_ORDER_PATH)

    # Plotting
    bp1.plot_profile(save_file_path=OUT_IMG1)
    bp2.plot_profile(save_file_path=OUT_IMG2)
    bp3.plot_profile(save_file_path=OUT_IMG3)

    cl = CellLine()
    cl.add_cell_line(bp1)
    cl.add_cell_line(bp2)
    cl.add_cell_line(bp3)

    cl.save_excel(output_file_path=OUTPUT)


if __name__ == '__main__':
    sys.exit(main())