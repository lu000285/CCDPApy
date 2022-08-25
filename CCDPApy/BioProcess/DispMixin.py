class DispMixin:
    # Display Methods
    # Display Experiment Info
    def disp_experiment(self):
        print('\n************ Experiment Information ************')
        print(f'Cell Line:              {self._cell_line_name}')
        print(f'Experiment ID:          {self._experiment_id}')
        print(f'Experimenter Name:      {self._experimenter_name}')
        print(f'Initial Culture Volume: {self._initial_volume} (mL)')
        print('Metabolite List:')
        if (self._spc_list):
            print(self._spc_list)
        else:
            print(self._original_spc_list)

    # Display Pre Process
    def disp_pre_process(self):
        print('************ Pre Process Data ************')
        print(self._pre_process)
        print('\n')

    # Display Cell
    def disp_cell_inpro_data(self):
        self._cell.disp_inpro_data()

    def disp_cell_post_twopt(self):
        self._cell.disp_post_data_twopt()

    def disp_cell_post_polyreg(self):
        self._cell.disp_polyreg()

    # Display Oxygen
    def disp_oxygen_inpro_data(self):
        self._oxygen.disp_inpro_data()

    def disp_oxygen_post_twopt(self):
        self._oxygen.disp_post_data_twopt()

    def disp_oxygen_post_polyreg(self):
        self._oxygen.disp_polyreg()

    # Display IgG
    def disp_igg_inpro_data(self):
        self._igg.disp_inpro_data()

    def disp_igg_post_twopt(self):
        self._igg.disp_post_data_twopt()

    def disp_igg_post_polyreg(self):
        self._igg.disp_polyreg()

    # Display Metabolite 
    def disp_aa_conc_data(self):
        n = len(self._aa_conc_df.columns)
        for i in range(0, n, 5):
            print('************ Metabolite Concentration Data ************')
            print(self._aa_conc_df.iloc[:, i:i+5])
            print('\n')

    def disp_aa_inpro_data(self):
        n = len(self._aa_df.columns)
        for i in range(0, n, 5):
            print('************ Metabolite Process Data ************')
            print(self._aa_df.iloc[:, i:i+5])
            print('\n')

    def disp_aa_post_twopt(self):
        n = len(self._post_twopt.columns)
        for i in range(0, n, 2):
            print('************ Metabolite Post Process Data -Two Point Calc. ************')
            print(self._post_twopt.iloc[:, i:i+2])
            print('\n')

    def disp_aa_post_polyreg(self):
        n = len(self._post_polyreg.columns)
        for i in range(0, n, 2):
            print('************ Metabolite Post Process Data -Poly. Reg. ************')
            print(self._post_polyreg.iloc[:, i:i+2])
            print('\n')

