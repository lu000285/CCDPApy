
class DispMixin:
    '''
    Disp Mixin class for BioProcess class.

    Methods
    -------
        disp_data(exp_info, process=[], spc=[])
    '''
    def disp_data(self, exp_info, process=[], spc=[]):
        '''
        Display data.
        Display the experiment information, pre-processed data, in-processed data, and post-processed data.

        Parameters
        ----------
            exp_info : bool
                pass true to display experiment information.
            process : str, list of str, default=[None], optional
                process name.
                use 'conc' for concentration data,
                'prepro' for pre-processed data,
                'inpro' for in-processed data,
                'twopt' for two-point calculation,
                'polyreg' for polynomial regression,
                'rollreg' for rolling polynomial regression.
            spc : str, list of str, default=[None], optional
                species name.
                use 'cell', 'oxygen', 'igg' or 'product', 'metabolite'.
        '''
        if type(process) == str:
            process = [process]
        if exp_info:
            self.__disp_experiment()
        if 'prepro' in process:
            self.__disp_pre_process()
            process.remove('prepro')
        if process:
            if 'cell' in spc:
                self.__disp_cell_data(process=process)
            if 'oxygen' in spc:
                self.__disp_oxy_data(process=process)
            if 'igg' in spc or 'product' in spc:
                self.__disp_igg_inpro_data(process=process)
            if 'metabolite' in spc:
                self.__disp_metabolite_data(process=process)


    # ******** Private Methods ******** #
    def __disp_experiment(self):
            '''Display experiment information.
            '''
            cell_line = self._md.cell_line_name
            exp_id = self._md.exp_id
            experimenter_name = self._md.exp_name
            initial_volume = self._md.initial_v
            print('\n************ Experiment Information ************')
            print(f'Cell Line:              {cell_line}')
            print(f'Experiment ID:          {exp_id}')
            print(f'Experimenter Name:      {experimenter_name}')
            print(f'Initial Culture Volume: {initial_volume} (mL)')
            print('Separate Feed List:')
            print(self._md.feed_list)
            print('Metabolite List:')
            if (self._spc_list):
                
                print(self._spc_list)

    def __disp_pre_process(self):
        '''Display pre-processed data.
        '''
        print('************ Pre Process Data ************')
        print(self._process_data_dict['prepro'])

    
    def __disp_cell_data(self, process):
        '''Display data for Cell
        '''
        if 'inpro' in process and self._process_flag_dict['inpro']:
            self._cell.disp_inpro_data()
        if 'twopt' in process and self._process_flag_dict['twopt']:
            self._cell.disp_post_data_twopt()
        if 'polyreg' in process and self._process_flag_dict['polyreg']:
            self._cell.disp_polyreg()

    
    def __disp_oxy_data(self, process):
        '''Display data for Oxygen
        '''
        if 'inpro' in process and self._process_flag_dict['inpro']:
            self._oxygen.disp_inpro_data()
        if 'twopt' in process and self._process_flag_dict['twopt']:
            self._oxygen.disp_post_data_twopt()
        if 'polyreg' in process and self._process_flag_dict['polyreg']:
            self._oxygen.disp_polyreg()


    def __disp_igg_inpro_data(self, process):
        '''Display data for Product/IgG
        '''
        if 'inpro' in process and self._process_flag_dict['inpro']:
            self._product.disp_inpro_data()
        if 'twopt' in process and self._process_flag_dict['twopt']:
            self._product.disp_post_data_twopt()
        if 'polyreg' in process and self._process_flag_dict['polyreg']:
            self._product.disp_polyreg()


    def __disp_metabolite_data(self, process):
        '''Display data for Metabolite
        '''
        if 'conc' in process and self._process_flag_dict['inpro']:
            print('************ Metabolite Concentration Data ************')
            print(self._spc_conc_df)
        if 'inpro' in process and self._process_flag_dict['inpro']:
            print('************ Metabolite In Process Data ************')
            #print(self._spc_df)
            print(self._process_data_dict['inpro'])
        if 'twopt' in process and self._process_flag_dict['twopt']:
            print('************ Metabolite Post Process Data -Two Point Calc. ************')
            print(self._process_data_dict['twopt'])
        if 'polyreg' in process and self._process_flag_dict['polyreg']:
            print('************ Metabolite Post Process Data -Poly. Reg. ************')
            print(self._process_data_dict['polyreg'])
        if 'rollreg' in process and self._process_flag_dict['rollreg']:
            print('************ Metabolite Post Process Data -Roll. Poly. Reg. ************')
            print(self._process_data_dict['rollreg'])

