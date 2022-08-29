from CCDPApy import CellLine    # used to aggregate all cell lines and experiments data
from CCDPApy import bio_process # used for data process of one experiment

data_file_1 = ['VS_NIIMBL VS-001.xlsx', 'VS_NIIMBL VS-002.xlsx', 'VS_NIIMBL VS-003.xlsx']
sheet_1 = 'Glutamine'
key_cl1 = {'use_feed_conc': True,
           'use_conc_after_feed': False,
           'spc_list': ['Glucose','Lactate','Glutamine','Asparagine','Aspartate'],
           'polyreg': True, 'polyorder_file': 'polynomial_order_1.xlsx',
           'rollreg': True, 'rollreg_order': 3, 'rollreg_window': 6,
           }

cell_line = CellLine()

for input in data_file_1:
    cl_1 = bio_process(input_file=input, measurement_sheet=sheet_1, **key_cl1)
    cell_line.add_bio_process(bio_process=cl_1)

data_file_2 = ['GS_Sigma_FB01_B1.xlsx', 'GS_Sigma_FB01_B2.xlsx', 'GS_Sigma_FB01_B3.xlsx']
sheet_2 = 'Glucose'
key_cl2 = {'use_feed_conc': False,
           'use_conc_after_feed': True,
           'spc_list': ['Glucose','Lactate','Glutamine','Asparagine','Aspartate'],
           'polyreg': True, 'polyorder_file': 'polynomial_order_2.xlsx',
           'rollreg': True, 'rollreg_order': 3, 'rollreg_window': 6,
           }
for input in data_file_2:
    cl_2 = bio_process(input_file=input, measurement_sheet=sheet_2, **key_cl2)
    cell_line.add_bio_process(bio_process=cl_2)

data_file_3 = ['Merck_XB50.xlsx', 'Merck_XB51.xlsx', 'Merck_XB52.xlsx']
sheet_3 = 'Glutamine'
key_cl3 = {'use_feed_conc': False,
           'use_conc_after_feed': False,
           'spc_list': ['Glucose','Lactate','Glutamine','Asparagine','Aspartate'],
           'all_method': True
           }

for input in data_file_3:
    cl_3 = bio_process(input_file=input, measurement_sheet=sheet_3, **key_cl3)
    cell_line.add_bio_process(bio_process=cl_3)

plot_list = ['Glucose','Lactate','Glutamine','Asparagine','Aspartate']

cell_line.save_excel(cell_line='GS CHOZN Clone 23', file_name='cl_1')
cell_line.save_excel(cell_line='GS Sigma CHOZN Clone 23', file_name='cl_2')
cell_line.save_excel(cell_line='Merck', file_name='cl_3')

cell_line.save_excel_rollreg(cell_line='GS CHOZN Clone 23', file_name='cl_1_rollreg')
cell_line.save_excel_rollreg(cell_line='GS Sigma CHOZN Clone 23', file_name='cl_2_rollreg')
cell_line.save_excel_rollreg(cell_line='Merck', file_name='cl_3_rollreg')



#fig = cell_line.plot_cell_lines(spc_list=plot_list, compare_cell_line=True)