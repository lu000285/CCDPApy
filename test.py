from CCDPApy import bio_process

key_cl1 = {'use_feed_conc': True,
           'use_conc_after_feed': False,
           #'spc_list': ['Glucose','Lactate','Glutamine','Asparagine','Aspartate'],
           'polyreg': True, 'polyorder_file': 'polynomial_order.xlsx',
           'rollreg': True, 'rollreg_order': 3, 'rollreg_window': 6,
           }

cl1_1 = bio_process(input_file='VS_NIIMBL VS-001.xlsx', **key_cl1)