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

    aa = ['Lactate', 'Glucose', 'Glutamine', 'Asparagine', 'Aspartate']
    POLY_ORDER_FILE = 'polynomial_order.xlsx'
    POLY_ORDER_PATH = os.path.join(BASE_DIR, POLY_ORDER_FILE)

    INPUT_SHEET = 'Measured Data'
    INPUT_FILE1 = 'GS_Sigma_FB01_B1.xlsx'     # File 1
    INPUT_FILE2 = 'GS_Sigma_FB01_B2.xlsx'     # File 2
    INPUT_FILE3 = 'GS_Sigma_FB01_B3.xlsx'     # File 3
    OUTPUT_FILE = 'Process.xlsx'

    IMG_FILE1 = 'CL2_0.png'
    IMG_FILE2 = 'CL2_1.png'
    IMG_FILE3 = 'CL2_2.png'

    INPUT_1  = os.path.join(BASE_DIR, INPUT_FILE1)
    INPUT_2  = os.path.join(BASE_DIR, INPUT_FILE2)
    INPUT_3  = os.path.join(BASE_DIR, INPUT_FILE3)
    OUT_IMG1 = os.path.join(BASE_DIR, IMG_FILE1)
    OUT_IMG2 = os.path.join(BASE_DIR, IMG_FILE2)
    OUT_IMG3 = os.path.join(BASE_DIR, IMG_FILE3)

    # Execute Bio Process
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

    bp1.plot_profile(save_file_path=OUT_IMG1)
    bp2.plot_profile(save_file_path=OUT_IMG2)
    bp3.plot_profile(save_file_path=OUT_IMG3)

    cl = CellLine()
    cl.add_cell_line(bp1)
    cl.add_cell_line(bp2)
    cl.add_cell_line(bp3)

    cl.save_excel(output_file_path=OUTPUT_FILE)


if __name__ == '__main__':
    sys.exit(main())