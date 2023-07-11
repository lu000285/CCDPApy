from CCDPApy import CellLine    # used to aggregate all cell lines and experiments data
from CCDPApy import bioprocess_pipeline
from CCDPApy import BioProcess

data_file_1 = ['CL1_1.xlsx', 'CL1_2.xlsx', 'CL1_3.xlsx']
key_cl1 = {'use_feed_conc': True,
           'use_conc_after_feed': False,
           #'spc_list': ['Glucose','Lactate','Glutamine','Asparagine','Aspartate'],
           'polyreg': True, 'polyorder_file': 'polynomial_order_1.xlsx',
           'rollreg': True, 'rollreg_order': 3, 'rollreg_window': 6,
           }

cell_line = CellLine()

'''for input in data_file_1:
    cl_1 = bioprocess_pipeline(input_file_name=input, **key_cl1)
    cell_line.add_bio_process(bio_process=cl_1)'''

data_file_2 = ['CL2_1.xlsx', 'CL2_2.xlsx', 'CL2_3.xlsx']
key_cl2 = {'use_feed_conc': False,
           'use_conc_after_feed': True,
           #'spc_list': ['Glucose','Lactate','Glutamine','Asparagine','Aspartate'],
           'polyreg': True, 'polyorder_file': 'polynomial_order_2.xlsx',
           'rollreg': True, 'rollreg_order': 3, 'rollreg_window': 6,
           }
for input in data_file_2:
    cl_2 = bioprocess_pipeline(input_file_name=input, **key_cl2)
    cell_line.add_bio_process(bio_process=cl_2)

data_file_3 = ['CL3_1.xlsx', 'CL3_2.xlsx', 'CL3_3.xlsx']
key_cl3 = {'use_feed_conc': False,
           'use_conc_after_feed': False,
           #'spc_list': ['Glucose','Lactate','Glutamine','Asparagine','Aspartate'],
           'polyreg': True, 'polyorder_file': 'polynomial_order_3.xlsx',
           'rollreg': True, 'rollreg_order': 3, 'rollreg_window': 6,
           }

'''for input in data_file_3:
    cl_3 = bioprocess_pipeline(input_file_name=input, **key_cl3)
    cell_line.add_bio_process(bio_process=cl_3)'''


#cell_line.save_excel(cell_line='Sample CL1', file_name='cl_1')
cell_line.save_excel(cell_line='Sample CL2', file_name='cl_2')
#cell_line.save_excel(cell_line='Sample CL3', file_name='cl_3')

#cell_line.save_excel_rollreg(cell_line='Sample CL1', file_name='cl_1_rollreg')
cell_line.save_excel_rollreg(cell_line='Sample CL2', file_name='cl_2_rollreg')
#cell_line.save_excel_rollreg(cell_line='Sample CL3', file_name='cl_3_rollreg')

'''cl1_1 = cell_line.get_cell_line(cl_name='Sample CL1')['Sample CL1_1']
cl1_1.disp_data(exp_info=True)'''