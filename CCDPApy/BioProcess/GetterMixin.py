import pandas as pd

class GetterMixin:
    '''
    '''
    # Get Cell Obj
    def get_cell(self):
        return self._cell
    
    # Get Oxygen obj
    def get_oxygen(self):
        return self._oxygen

    # Get IgG obj
    def get_product(self):
        return self._product

    # Get Cell Line Name
    def get_cell_line(self):
        return self._md.cell_line_name

    # Get Experiment ID
    def get_exp_id(self):
        return self._md.exp_id

    # Get Experiment Infomation DF
    def get_exp_info(self):
        return self._exp_info

    def get_measured_data_dict(self):
        '''Return measured data dictionary.
        '''
        return self._measured_data_dict

    def get_measured_data_df(self):
        '''Return measured data DataFrame.
        '''
        return self._measured_data_df

    # Get Poly. Reg. Order DF
    def get_polyreg_order_df(self):
        return self._polyorder_df

    # Get Pre Process DF
    def get_pre_process(self):
        return self._pre_process

    # Get In Process DF
    def get_in_process(self):
        blank = pd.Series(data=pd.NA, name='*********')
        self._in_process = pd.concat([self._process_data_dict['prepro'],
                                      blank,
                                      self._cell.get_ivcc(),
                                      self._cell.get_cumulative(),
                                      self._oxygen.get_cumulative(),
                                      self._product.get_cumulative(),
                                      self._process_data_dict['inpro'],
                                      self._conc_after_feed_df],
                                      axis=1)
        return self._in_process

    # Get Metabolite List
    def get_spc_list(self):
        return self._spc_list

    # Get Original Metabolite List
    def get_default_spc_list(self):
        return self._default_spc_list

    # Get Metabolite dictionary
    def get_spc_dict(self):
        return self._spc_dict

    # Get Metabolite Concentration DF
    def get_spc_conc(self):
        return self._spc_conc_df

    '''# Get Metabolite Cumulative DF
    def get_spc_df(self):
        return self._spc_df'''

    def get_process_data(self, method):
        '''
        Get processed data.

        Parameters
        ---------
            method : str
                name of the method of post process.
                'prepro'
                'inpro'
                'twopt',
                'polyreg', 
                'rollreg'.
        Returns
        -------
            pandas.DataFrame
        '''
        return self._process_data_dict[method]

    # Get BioProcess DF
    def get_bioprocess_df(self):
        in_pro = self.get_in_process()
        blank = pd.Series(data=pd.NA, name='*********')
        return pd.concat([self._cl_col,
                          self._expID_col,
                          self._md.data_df,
                          blank,
                          in_pro,
                          blank,
                          self._oxygen.get_oxy_post_data(),
                          self._cell.get_post_data_twopt(),
                          self._product.get_sp_rate(method='twopt'),
                          self._process_data_dict['twopt'],
                          blank,
                          self._oxygen.get_sp_rate(method='polyreg'),
                          self._product.get_sp_rate(method='polyreg'),
                          self._process_data_dict['polyreg']],
                          axis = 1)