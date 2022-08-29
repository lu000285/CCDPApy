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
        if self._pre_process_flag:
            print('************ Pre Process Data ************')
            print(self._pre_process)
        else:
            print('Pre Process Not Yet Done.')

    # Display Data
    def disp_data(self, spc, process):
        '''
        '''
        if spc=='cell':
            self._disp_cell_data(process=process)
        elif spc=='oxygen':
            self._disp_oxy_data(process=process)
        elif spc=='igg' or spc=='product':
            self._disp_igg_inpro_data(process=process)
        elif spc=='metabolite':
            self._disp_metabolite_data(process=process)
        else:
            print(f'{spc} {process} Not Yet Done.')


# ******** Private Methods ******** #
    # Display data for Cell
    def _disp_cell_data(self, process):
        if process=='inpro' and self._in_process_flag:
            self._cell.disp_inpro_data()
        elif process=='twopt' and self._twopt_flag:
            self._cell.disp_post_data_twopt()
        elif process=='polyreg' and self._polyreg_flag:
            self._cell.disp_polyreg()
        else:
            print(f'{process} Not Yet Done.')

    # Display data for Oxygen
    def _disp_oxy_data(self, process):
        if process=='inpro' and self._in_process_flag:
            self._oxygen.disp_inpro_data()
        elif process=='twopt' and self._twopt_flag:
            self._oxygen.disp_post_data_twopt()
        elif process=='polyreg' and self._polyreg_flag:
            self._oxygen.disp_polyreg()
        else:
            print('In Process Not Yet Done.')

    # Display data for Product/IgG
    def _disp_igg_inpro_data(self, process):
        if process=='inpro' and self._in_process_flag:
            self._igg.disp_inpro_data()
        elif process=='twopt' and self._twopt_flag:
            self._igg.disp_post_data_twopt()
        elif process=='polyreg' and self._polyreg_flag:
            self._igg.disp_polyreg()
        else:
            print('In Process Not Yet Done.')

    # Display data for Metabolite
    def _disp_metabolite_data(self, process):
        if process=='conc' and self._in_process_flag:
            print('************ Metabolite Concentration Data ************')
            print(self._spc_conc_df)
        elif process=='inpro' and self._in_process_flag:
            print('************ Metabolite In Process Data ************')
            print(self._spc_df)
        elif process=='twopt' and self._twopt_flag:
            print('************ Metabolite Post Process Data -Two Point Calc. ************')
            print(self._post_twopt)
        elif process=='polyreg' and self._polyreg_flag:
            print('************ Metabolite Post Process Data -Poly. Reg. ************')
            print(self._post_polyreg)
        elif process=='rollreg' and self._rollreg_flag:
            print('************ Metabolite Post Process Data -Roll. Poly. Reg. ************')
            print(self._post_rollpolyreg)
        else:
            print(f'{process} Not Yet Done.')

