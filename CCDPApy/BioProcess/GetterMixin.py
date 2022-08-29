import pandas as pd

class GetterMixin:
    # Get Cell Obj
    def get_cell(self):
        return self._cell
    
    # Get Oxygen obj
    def get_oxygen(self):
        return self._oxygen

    # Get IgG obj
    def get_igg(self):
        return self._igg

    # Get Cell Line Name
    def get_cell_line(self):
        return self._cell_line_name

    # Get Experiment ID
    def get_exp_id(self):
        return self._experiment_id

    # Get Experiment Infomation DF
    def get_exp_info(self):
        return self._exp_info

    # Get Measured Data DF
    def get_measured_data(self):
        return self._measured_data

    # Get Poly. Reg. Order DF
    def get_polyreg_order_df(self):
        return self._polyorder_df

    # Get Pre Process DF
    def get_pre_process(self):
        return self._pre_process

    # Get In Process DF
    def get_in_process(self):
        blank = pd.Series(data=pd.NA, name='*********')
        self._in_process = pd.concat([self._pre_process,
                                      blank,
                                      self._cell.get_ivcc(),
                                      self._cell.get_cumulative(),
                                      self._oxygen.get_cumulative(),
                                      self._igg.get_cumulative(),
                                      self._spc_df,
                                      self._conc_after_feed_df],
                                      axis=1)
        return self._in_process

    # Get Metabolite List
    def get_spc_list(self):
        if (self._spc_list):
            return self._spc_list
        else:
            return self._original_spc_list

    # Get Original Metabolite List
    def get_original_spc_list(self):
        return self._original_spc_list

    # Get Metabolite dictionary
    def get_spc_dict(self):
        return self._spc_dict

    def get_special_spc_dict(self):
        return self._special_spc_dict

    # Get Metabolite Concentration DF
    def get_spc_conc(self):
        return self._spc_conc_df

    # Get Metabolite Cumulative DF
    def get_spc_df(self):
        return self._spc_df

    # Get Post Process DF
    def get_twopt_df(self):
        return self._post_twopt

    # Get Post Process DF
    def get_polyreg_df(self):
        return self._post_polyreg

    def get_rollreg_df(self):
        return self._post_rollpolyreg

    # Get BioProcess DF
    def get_bioprocess_df(self):
        in_pro = self.get_in_process()
        blank = pd.Series(data=pd.NA, name='*********')
        return pd.concat([self._cl_col,
                          self._expID_col,
                          self._measured_data,
                          blank,
                          in_pro,
                          blank,
                          self._oxygen.get_oxy_post_data(),
                          self._cell.get_post_data_twopt(),
                          self._igg.get_sp_rate(method='twopt'),
                          self._post_twopt,
                          blank,
                          self._oxygen.get_sp_rate(method='polyreg'),
                          self._igg.get_sp_rate(method='polyreg'),
                          self._post_polyreg],
                          axis = 1)

    # Get Rolling Polynomial Regression DF
    def get_post_rollpolyreg(self):
        return self._post_rollpolyreg
