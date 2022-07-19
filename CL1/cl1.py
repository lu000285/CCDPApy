import sys

from test_package.BioProcess.CellLine import CellLine
from test_package.BioProcess.bio_process import bio_process as BP
from test_package.pre_process.pre_process import pre_process
from test_package.in_process.in_process import cumulative_in_pro
from test_package.post_process.two_point_calc.twopt_post_process import twopt_post_process
from test_package.post_process.polynomial_regression.polynomial_regression import polyreg_post_pro
from test_package.post_process.rolling_regression.rolling_regression import rolling_regression

# Main Function
def main():
    # AA List to Analyze; If not specified, all AAs are analyzed.
    aa_lst = ['Glucose','Lactate','Glutamine','Asparagine','Aspartate']

    #****** BioProcess Obj *******
    bp = BP(input_file_name='VS_NIIMBL VS-001.xlsx',
            measured_data_sheet_name='Measured Data',
            aa_list=aa_lst)

    bp2 = BP(input_file_name='VS_NIIMBL VS-002.xlsx',
            measured_data_sheet_name='Measured Data',
            aa_list=aa_lst)
    
    bp3 = BP(input_file_name='VS_NIIMBL VS-003.xlsx',
            measured_data_sheet_name='Measured Data',
            aa_list=aa_lst)

    #****** Pre Process ******
    bp = pre_process(bio_process=bp)
    bp2 = pre_process(bio_process=bp2)
    bp3 = pre_process(bio_process=bp3)

    #****** In Process -Cumulative Cons/Prod ******
    # Use Feed Conc.
    bp = cumulative_in_pro(bio_process=bp, use_feed_conc=True, use_conc_after_feed=False)
    bp2 = cumulative_in_pro(bio_process=bp2, use_feed_conc=True, use_conc_after_feed=False)
    bp3 = cumulative_in_pro(bio_process=bp3, use_feed_conc=True, use_conc_after_feed=False)

    #***** Post Process -SP. Rate Two Point Calc ******
    bp = twopt_post_process(bio_process=bp)
    bp2 = twopt_post_process(bio_process=bp2)
    bp3 = twopt_post_process(bio_process=bp3)

    #***** Post Process -SP. Rate Poly. Regression *****
    bp = polyreg_post_pro(bio_process=bp, polyorder_file='polynomial_order.xlsx')
    bp2 = polyreg_post_pro(bio_process=bp2, polyorder_file='polynomial_order.xlsx')
    bp3 = polyreg_post_pro(bio_process=bp3, polyorder_file='polynomial_order.xlsx')
    
    #****** Cell Line Obj *******
    cl = CellLine('CL1')
    #***** Add each bio processs to Cell Line obj *****
    cl.add_cell_line(bio_process=bp)
    cl.add_cell_line(bio_process=bp2)
    cl.add_cell_line(bio_process=bp3)

    #***** Display Info *****
    # cl.disp_cell_lines()

    #***** Saving *****
    cl.save_excel(file_name='CL1_BioProcess')

    #***** Plotting - Multiple Species *****
    plot_list = ['lactate', 'glucose', 'glutamine', 'asparagine', 'aspartate']
    bp.plot_profile(aa_list=plot_list, save_file_name='CL1_1')
    bp2.plot_profile(aa_list=plot_list, save_file_name='CL1_2')
    bp3.plot_profile(aa_list=plot_list, save_file_name='CL1_3')

    #***** Post Process -SP. Rate Rolling Poly. Regression *****
    r_lst = ['rglut1','rmct','rglnna','rasnna','raspna']
    aa_lst = ['Glucose','Lactate','Glutamine','Asparagine','Aspartate']
    # Window Size: 6
    bp_ws6 = rolling_regression(bio_process=bp, order=3, windows=6, aa_lst=aa_lst, r_lst=r_lst)
    bp2_ws6 = rolling_regression(bio_process=bp2, order=3, windows=6, aa_lst=aa_lst, r_lst=r_lst)
    bp3_ws6 = rolling_regression(bio_process=bp3, order=3, windows=6, aa_lst=aa_lst, r_lst=r_lst)
    
    #****** Cell Line Obj with Rolling Reg. for Window Size of 6 *******
    cl_ws6 = CellLine('CL1_Rolling_Reg_WS6')
    #***** Add each bio processs to Cell Line obj *****
    cl_ws6.add_cell_line(bp_ws6)
    cl_ws6.add_cell_line(bp2_ws6)
    cl_ws6.add_cell_line(bp3_ws6)

    #***** Saving *****
    cl_ws6.save_excel_rolling_reg(file_name='CL1_Rolling_Reg_WS6')

    #***** Plotting - Multiple Species *****
    plot_list = ['lactate', 'glucose', 'glutamine', 'asparagine', 'aspartate']    
    # With Rolliig Poly. Reg with Saving
    bp_ws6.plot_profile(aa_list=plot_list, save_file_name='CL1_1_ws_6', rolling=True)
    bp2_ws6.plot_profile(aa_list=plot_list, save_file_name='CL1_2_ws_6', rolling=True)
    bp3_ws6.plot_profile(aa_list=plot_list, save_file_name='CL1_3_ws_6', rolling=True)

    #***** Post Process -SP. Rate Rolling Poly. Regression *****
    # Window Size: 8
    bp_ws8 = rolling_regression(bio_process=bp, order=3, windows=8, aa_lst=aa_lst, r_lst=r_lst)
    bp2_ws8 = rolling_regression(bio_process=bp2, order=3, windows=8, aa_lst=aa_lst, r_lst=r_lst)
    bp3_ws8 = rolling_regression(bio_process=bp3, order=3, windows=8, aa_lst=aa_lst, r_lst=r_lst)

    #****** Cell Line Obj *******
    cl_ws8 = CellLine('CL1_Rolling_Reg_WS8')
    #***** Add each bio processs to Cell Line obj *****
    cl_ws8.add_cell_line(bp_ws8)
    cl_ws8.add_cell_line(bp2_ws8)
    cl_ws8.add_cell_line(bp3_ws8)

    #***** Saving *****
    cl_ws8.save_excel_rolling_reg(file_name='CL1_Rolling_Reg_WS8')

    #***** Plotting - Multiple Species *****
    plot_list = ['lactate', 'glucose', 'glutamine', 'asparagine', 'aspartate']    
    # With Rolliig Poly. Reg with Saving
    bp_ws8.plot_profile(aa_list=plot_list, save_file_name='CL1_1_ws_8', rolling=True)
    bp2_ws8.plot_profile(aa_list=plot_list, save_file_name='CL1_2_ws_8', rolling=True)
    bp3_ws8.plot_profile(aa_list=plot_list, save_file_name='CL1_3_ws_8', rolling=True)




if __name__ == '__main__':
    sys.exit(main())