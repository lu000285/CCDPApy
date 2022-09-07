from CCDPApy import CellLine    # used to aggregate all cell lines and experiments data
from CCDPApy import bioprocess_pipeline
from CCDPApy.BioProcess.BioProcess import BioProcess

input = ['CL1_1.xlsx', 'CL1_2.xlsx', 'CL1_2.xlsx']
measurement_sheet = 'Measured Data'
feed_sheet = 'Separate Feed Info'
poly_file = 'polynomial_order_1.xlsx'
spc = ['Glucose','Lactate','Glutamine','Asparagine','Aspartate']
new = ['new']


bp = BioProcess(file_name='CL1_1.xlsx',
                measurement_sheet=measurement_sheet,
                feed_sheet=feed_sheet,
                #spc_list=spc,
                #new_spc_list=new
                )
s = ['cell', 'igg', 'oxygen']
m = 'metabolite'

bp.inprocess(use_feed_conc=True, use_conc_after_feed=False)

# bp.disp_data(exp_info=True, process=['prepro'])
# bp.disp_data(exp_info=True, process=['inpro'], spc=s)

#bp.two_pt_calc()
# bp.disp_data(exp_info=True, process=['twopt'], spc=s)
# bp.disp_data(exp_info=True, process=['twopt'], spc='metabolite')

#bp.poly_regression(polyorder_file=poly_file)
# bp.disp_data(exp_info=True, process=['polyreg'], spc='metabolite')

bp.roll_regression(order=3, windows=6)
# bp.disp_data(exp_info=True, process=['rollreg'], spc='metabolite')

# bp.save_excel('cl1.xlsx')
bp.save_excel_rollreg('rollreg.xlsx')

cl = CellLine()
cl.add_bio_process(bio_process=bp)
cl.disp_cell_lines()

'''plot_list = ['cell', 'alanine']
profile = ['conc', 'cumulative']
profile = 'cumulative'
fig = bp.plot(spc_list=plot_list, profile=profile, viability=True, )

key = {'use_feed_conc': True,
       'use_conc_after_feed': False,
       'spc_list': ['Glucose','Lactate','Glutamine','Asparagine','Aspartate'],
       'polyreg': True, 'polyorder_file': 'polynomial_order_1.xlsx',
       'rollreg': True, 'rollreg_order': 4, 'rollreg_window': 7,
        }
bp = bioprocess_pipeline(input_file_name=input[0],
                         measurement_sheet=measurement_sheet,
                         feed_sheet=feed_sheet,
                         **key)
bp.disp_data(exp_info=True, process=['inpro'], spc='metabolite')'''