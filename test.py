from CCDPApy import CellLine    # used to aggregate all cell lines and experiments data
from CCDPApy import bio_process # used for data process of one experiment

from CCDPApy.pre_process.pre_process import pre_process
from CCDPApy.in_process.in_process import cumulative_calc
from CCDPApy.post_process.two_point_calc.twopt_calc import twopt_calc
from CCDPApy.post_process.polynomial_regression.polynomial_regression import polyreg_calc
from CCDPApy.post_process.rolling_regression.rolling_regression import rolling_regression


data_file_2 = ['GS_Sigma_FB01_B1.xlsx', 'GS_Sigma_FB01_B2.xlsx', 'GS_Sigma_FB01_B3.xlsx']
sheet_2 = 'Glucose'
poly_file = 'polynomial_order_2.xlsx'
spc = ['alanine', 'glucose']

cl2_1 = bio_process(input_file=data_file_2[0],
                    measurement_sheet=sheet_2,
                    #spc_list=spc
                    )

# ************** Test Pre Process ************** #
pre_process(bio_process=cl2_1, feed_name=sheet_2)

# Test Disp Method
cl2_1.disp_experiment()
cl2_1.disp_pre_process()


# ************** Test In Process ************** #
cumulative_calc(bio_process=cl2_1,
                feed_name=sheet_2,
                use_feed_conc=False,
                use_conc_after_feed=True)

# Test Disp Method
'''cl2_1.disp_cell_inpro_data()
cl2_1.disp_oxygen_inpro_data()
cl2_1.disp_igg_inpro_data()
cl2_1.disp_conc_data()
cl2_1.disp_inpro_data()'''


# ************** Test Post Process ************** #
# ************** Two-Point Calc. ************** #
twopt_calc(bio_process=cl2_1)

# Test Disp Method
# cl2_1.disp_twopt_data()

# ************** Poly. Reg. ************** #
polyreg_calc(bio_process=cl2_1, polyorder_file=poly_file)

# Test Disp Method
# cl2_1.disp_polyreg_data()

# ************** Roll. Poly. Reg. ************** #
rolling_regression(bio_process=cl2_1, order=3, windows=6)

# Test Disp Method
'''aln = cl2_1.get_spc_dict()['GLUCOSE']
print(aln.get_sp_rate('rollreg'))'''

'''
cl2_1.rollreg(order=3, windows=6)

aln = cl2_1.get_spc_dict()['ALANINE']
print(aln.get_rollpolyreg_sp_rate())'''
