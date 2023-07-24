from CCDPApy import CellLine    # used to aggregate all cell lines and experiments data
from CCDPApy import bioprocess_pipeline
from CCDPApy.cell_line.Fed_batch.BioProcess import BioProcess

input_files = ['04-A1.xlsx', '04-B1.xlsx', '04-C1.xlsx', 'GS_SF13.xlsx']
measurement_sheet = 'Measured Data'
feed_sheet = 'Separate Feed Info'
key = {'use_feed_conc': True,
       'use_conc_after_feed': False,
       'spc_list': ['Glucose','Lactate','Glutamine'],
       'polyreg': True, 
       'rollreg': True, 'rollreg_order': 3, 'rollreg_window': 6,
        }

bio_process = bioprocess_pipeline(input_file_name='GS_SF13.xlsx',
                                  measurement_sheet=measurement_sheet,
                                  feed_sheet=feed_sheet,
                                  **key
                                  )
bio_process.disp_data(exp_info=True)

#bio_process.disp_data(exp_info=False, process=['prepro'])
#bio_process.disp_data(exp_info=False, process=['inpro'], spc=['metabolite'])
#bio_process.disp_data(exp_info=False, process=['twopt'], spc=['metabolite'])
#bio_process.disp_data(exp_info=False, process=['polyreg'], spc=['metabolite'])
#bio_process.disp_data(exp_info=False, process=['rollreg'], spc=['metabolite'])
