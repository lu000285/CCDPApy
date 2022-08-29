import sys
from CCDPApy import bio_process
from CCDPApy import CellLine

def main():
        key_cl1 = {'use_feed_conc': True,
                   'use_conc_after_feed': False,
                   'aa_list': ['Glucose','Lactate','Glutamine','Asparagine','Aspartate'],
                   'polyreg': True, 'polyorder_file': 'polynomial_order.xlsx',
                   'rollreg': True, 'rollreg_order': 3, 'rollreg_window': 6,
                   }

        cl1_1 = bio_process(input_file='VS_NIIMBL VS-001.xlsx', **key_cl1)
        cl1_2 = bio_process(input_file='VS_NIIMBL VS-002.xlsx', **key_cl1)
        cl1_3 = bio_process(input_file='VS_NIIMBL VS-003.xlsx', **key_cl1)

        key_cl2 = {'use_feed_conc': False,
                'use_conc_after_feed': True,
                'aa_list': ['Glucose','Lactate','Glutamine','Asparagine','Aspartate'],
                'polyreg': True, 'polyorder_file': 'polynomial_order.xlsx'
                }

        cl2_1 = bio_process(input_file='GS_Sigma_FB01_B1.xlsx', **key_cl2)
        cl2_2 = bio_process(input_file='GS_Sigma_FB01_B2.xlsx', **key_cl2)
        cl2_3 = bio_process(input_file='GS_Sigma_FB01_B3.xlsx', **key_cl2)

        key_cl3 = {'use_feed_conc': False,
                'use_conc_after_feed': False,
                'aa_list': ['Glucose','Lactate','Glutamine','Asparagine','Aspartate'],
                'polyreg': True, 'polyorder_file': 'polynomial_order.xlsx'
                }

        cl3_1 = bio_process(input_file='Merck_XB50.xlsx', **key_cl3)
        cl3_2 = bio_process(input_file='Merck_XB51.xlsx', **key_cl3)
        cl3_3 = bio_process(input_file='Merck_XB52.xlsx', **key_cl3)

        cell_line = CellLine()
        cell_line.add_bio_process(bio_process=cl1_1)
        cell_line.add_bio_process(bio_process=cl1_2)
        cell_line.add_bio_process(bio_process=cl1_3)
        cell_line.add_bio_process(bio_process=cl2_1)
        cell_line.add_bio_process(bio_process=cl2_2)
        cell_line.add_bio_process(bio_process=cl2_3)
        cell_line.add_bio_process(bio_process=cl3_1)
        cell_line.add_bio_process(bio_process=cl3_2)
        cell_line.add_bio_process(bio_process=cl3_3)

        # aa = ['Glucose','Lactate','Glutamine','Asparagine','Aspartate']
        aa = ['Asparagine']
        cl = 'GS CHOZN Clone 23'
        method = ['polyreg', 'rollreg']

        fig = cell_line.plot(cell_line=cl, aa_lst=aa, method=method)

        fig = cell_line.plot2(aa_list=aa, compare_cell_line=True, method='polyreg')

        method = ['twopt', 'polyreg']
        # method = ['all']
        fig = cell_line.plot2(aa_list=aa, compare_cell_line=False, method=method)

        cell_line.save_excel(cell_line='GS CHOZN Clone 23', file_name='cl1')
        cell_line.save_excel(cell_line='GS Sigma CHOZN Clone 23', file_name='cl2')
        cell_line.save_excel(cell_line='Merck', file_name='cl3')


if __name__ == '__main__':
    sys.exit(main())
