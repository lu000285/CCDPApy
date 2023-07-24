class SetterMixin:
    '''
    Setters Mixin class for BioProcess class.

    Methods
    ------
        set_process_flag(process, flag)
            set flag for biorpocess.
        set_cell
        set_oxygen
        set_igg
        set_spc_df
        set_spc_conc
        set_spc_conc_after_feed
        set_spc_dict
        set_spc_list
        set_new_spc
        set_process_data
    '''
    def set_process_flag(self, process, flag):
        '''
        set a flag (True/False) for the bioprocess.

        Parameters
        ----------
            process : str
                process name.
                use 'inpro' for in-process, 
                'twopt' for two-point calculation, 
                'polyreg' for polynomial regression,
                'rollreg' for rolling polynomial regression.
            flag : bool
        '''
        self._process_flag_dict[process] = flag

    def set_cell(self, cell):
        self._cell = cell

    def set_oxygen(self, oxygen):
        self._oxygen = oxygen

    def set_igg(self, igg):
        self._igg = igg

    def set_spc_df(self, spc_df):
        self._spc_df = spc_df

    def set_spc_conc(self, conc):
        self._spc_conc_df = conc
        
    def set_spc_conc_after_feed(self, conc_after_feed):
        self._conc_after_feed_df = conc_after_feed

    def set_process_data(self, process, data):
        '''
        Set processed data for each process.

        Parameters
        ----------
            process : str
                process name.
                use 'inpro' for in-process, 
                'twopt' for two-point calculation, 
                'polyreg' for polynomial regression,
                'rollreg' for rolling polynomial regression.
            data : pandas.DataFrame
                processed data.
        '''
        self._process_data_dict[process] = data.copy()

    def set_polyorder_df(self, polyorder_df):
        self._polyorder_df = polyorder_df