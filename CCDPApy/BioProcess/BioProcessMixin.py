import pandas as pd

from ..helper_func.helper_func import output_path
from ..post_process.polynomial_regression.polynomial_regression import polyreg_calc
from ..post_process.rolling_regression.rolling_regression import rolling_regression


class BioProcessMixin():
    '''
    Methods
    -------
        regression : 
        save_excel : 
        save_excel_rollpolyreg : 
    '''
    def regression(self, method,
                   polyorder_file=None,
                   rollreg_prop={'order': 3, 'windows': 6}
                   ):
        '''
        Calculate SP. rate for species using a regression method.
        Polynomial regression, and rolling polynomial regression can be used.

        Parameters
        ----------
            method : str
                name of the regression method.
                use 'polyreg', 'rollreg'.
            polyoder_file : str, default=None, optional
                an Excel file name for the polynomial regression order.
            rollreg_prop : dictionary, default={'order': 3, 'windows': 6}, optional
                propertyr for rolling polynomial regression.
                use {'order': int, 'windows': int}
        '''
        if method=='polyreg':
            polyreg_calc(bio_process=self, polyorder_file=polyorder_file)
        elif method=='rollreg':
            order = rollreg_prop['order']
            windows = rollreg_prop['windows'] 
            rolling_regression(bio_process=self, order=order, windows=windows)
        else:
            print(f'cannot process regression with this {method} method.')


    def save_excel(self, file_name):
        '''
        Save the bioprocess data as an Excel file.
        Please include '.xlsx'.
        Do not include rolling regression data. To save the rolling regression data,
        use save_excel_rollpolyreg method. 

        Parameters
        ----------
        file_name : str
            File name.
            Please include '.xlsx'.
        '''
        file_path = output_path(file_name=file_name)
        out_df = self.get_bioprocess_df()

        # Save
        out_df.to_excel(file_path, sheet_name=self._md.exp_id, index=False)
        print(f'{file_name} Saved.\n')


    # Saveing Rolling PolyReg Method
    def save_excel_rollreg(self, file_name):
        '''
        Save rolling regression data as an Excel file.
        Please include '.xlsx'.
        Do not include other bioprocess data. To save other data,
        use save_excel.

        Parameters
        ----------
        file_name : str
            File name.
            Please include '.xlsx'.
        '''
        if '.xlsx' not in file_name:
            file_name += '.xlsx'
        file_path = output_path(file_name=file_name)
        out_df = self.get_process_data('rollreg')
        # Save
        print(f'{file_name} Saving......')
        out_df.to_excel(file_path, sheet_name=self._md.exp_id, index=False)
        print(f'{file_name} Saved.\n')

# End BioProcessMixin
