class SetterMixin:
    # Setters
    def set_polyreg_order_df(self, order_df):
        self._polyorder_df = order_df

    def set_cell(self, cell):
        self._cell = cell
        self._pre_process = cell.get_pre_data()

    def set_oxygen(self, oxygen):
        self._oxygen = oxygen
        self._pre_process = oxygen.get_pre_data()

    def set_igg(self, igg):
        self._igg = igg
        self._pre_process = igg.get_pre_data()

    def set_aa_df(self, aa_df):
        self._aa_df = aa_df

    def set_aa_conc(self, conc):
        self._aa_conc_df = conc
        
    def set_aa_conc_after_feed(self, conc_after_feed):
        self._conc_after_feed_df = conc_after_feed

    def set_aa_dict(self, aa_dict):
        self._aa_dict = aa_dict

    def set_aa_list(self, aa_list):
        self._aa_list = aa_list

    def set_new_spc(self, new_spc_list):
        for new_spc in new_spc_list:
            self._original_aa_list.append(new_spc)

    def set_pre_process(self, pre_process):
        self._pre_process = pre_process

    def set_in_process(self, in_process):
        self._in_process = in_process

    def set_post_twopt(self, twopt):
        self._post_twopt = twopt

    def set_post_polyreg(self, polyreg):
        self._post_polyreg = polyreg

    def set_polyorder_df(self, polyorder):
        self._polyorder_df = polyorder

    def set_post_rollpolyreg(self, rollpolyreg):
        self._post_rollpolyreg = rollpolyreg