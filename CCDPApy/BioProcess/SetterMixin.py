class SetterMixin:
    # Setters
    def set_process_flag(self, process, flag):
        if process=='pre':
            self._pre_process_flag = flag
        elif process=='in':
            self._in_process_flag = flag
        elif process=='twopt':
            self._twopt_flag = flag
        elif process=='polyreg':
            self._polyreg_flag = flag
        elif process=='rollreg':
            self._rollreg_flag = flag


    def set_feed_added(self, feed_added):
        self._feed_added = feed_added

    def set_cell(self, cell):
        self._cell = cell
        self._pre_process = cell.get_pre_data()

    def set_oxygen(self, oxygen):
        self._oxygen = oxygen
        self._pre_process = oxygen.get_pre_data()

    def set_igg(self, igg):
        self._igg = igg
        self._pre_process = igg.get_pre_data()

    def set_spc_df(self, spc_df):
        self._spc_df = spc_df

    def set_spc_conc(self, conc):
        self._spc_conc_df = conc
        
    def set_spc_conc_after_feed(self, conc_after_feed):
        self._conc_after_feed_df = conc_after_feed

    def set_spc_dict(self, spc_dict):
        self._spc_dict = spc_dict

    def set_spcial_spc_dict(self, spc_dict):
        self._special_spc_dict = spc_dict

    def set_spc_list(self, spc_list):
        self._spc_list = spc_list

    def set_new_spc(self, new_spc_list):
        for new_spc in new_spc_list:
            self._original_spc_list.append(new_spc)

    def set_pre_process_df(self, pre_process_df):
        self._pre_process = pre_process_df

    def set_in_process_df(self, in_process_df):
        self._in_process = in_process_df

    def set_twopt_df(self, twopt_df):
        self._post_twopt = twopt_df

    def set_polyreg_df(self, polyreg_df):
        self._post_polyreg = polyreg_df

    def set_polyorder_df(self, polyorder_df):
        self._polyorder_df = polyorder_df

    def set_rollreg_df(self, rollreg_df):
        self._post_rollpolyreg = rollreg_df