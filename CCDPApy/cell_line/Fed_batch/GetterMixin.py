import pandas as pd

class GetterMixin:
    '''
    '''
    @property
    def use_feed_conc(self):
        return self._use_feed_conc
    @property
    def use_conc_after_feed(self):
        return self._use_conc_after_feed
    @property
    def cell_line(self):
        '''Return cell line name.'''
        return self._cell_line
    @property
    def id(self):
        '''Return experiment ID.'''
        return self._exp_id

    def get_species(self, species):
        '''Return species object.
        '''
        spc = self._spc_dict
        key = species.lower()
        if key=='all':
            return spc
        elif key in spc.keys() or key=='igg':
            return spc[key]
        else:
            print("Wrong species name. Please check below.")
            print(spc.keys())

    def get_conc_df(self):
        data = self.conc.copy()
        data['Cell Line'] = self.cell_line
        data['ID'] = self.id
        return data
    
    def get_cumulative_conc_df(self):
        data = self.cumulative_conc.copy()
        data['Cell Line'] = self.cell_line
        data['ID'] = self.id
        return data
    
    def get_sp_rate_df(self):
        data = self.sp_rate.copy()
        data['Cell Line'] = self.cell_line
        data['ID'] = self.id
        return data
    
    def get_cell_data_df(self):
        cell = self.get_species('cell')
        conc = cell.conc.copy()
        conc['Cell Line'] = self.cell_line
        conc['ID'] = self.id

        ivcc = cell.integral_viable_cell_conc.copy()
        ivcc['Cell Line'] = self.cell_line
        ivcc['ID'] = self.id

        cumlative = cell.cumulative_conc.copy()
        cumlative['Cell Line'] = self.cell_line
        cumlative['ID'] = self.id

        rate = cell.sp_rate.copy()
        rate['Cell Line'] = self.cell_line
        rate['ID'] = self.id
        return conc, ivcc, cumlative, rate

    '''def get_in_process_data(self):
        Return In-Process data.
        spc = self.get_species('all')
        df_list = []
        for name, s in spc.items():
            df = s.get_in_process_data
            df['species'] = name.capitalize()
            df_list.append(df)
        data = pd.concat(df_list, axis=0).reset_index(drop=True)
        data['Cell Line'] = self.cell_line
        data['ID'] = self.id
        data = data[['cellLine', 'runID', 'runTime', 'species', 'value', 'profile', 'kind', 'method']]
        return data'''
    
    '''def get_post_process_data(self):
        #Return Post-Process data.
        spc = self._spc_dict.copy()
        data = None

        # Polynomial
        if self._process_flag_dict['polyreg']:
            df_list = []
            for name, s in spc.items():
                df = s.get_post_process_data
                df['species'] = name.lower()
                df_list.append(df)
            data = pd.concat(df_list, axis=0).reset_index(drop=True)
            data['cellLine'] = self._cell_line
            data['runID'] = self._exp_id
            data = data[['cellLine', 'runID', 'runTime', 'species', 'value', 'profile', 'kind', 'method']]

        # Rolling polynomial
        if self._process_flag_dict['rollreg']:
            cell = spc.pop('cell'.upper())
            oxygen = spc.pop('oxygen'.upper())
            df_list = []
            growth_rate = cell.get_post_process_logistic
            growth_rate['species'] = 'cell'
            df_list.append(growth_rate)

            for name, s in spc.items():
                df = s.get_post_process_roll_data
                df['species'] = name.lower()
                df_list.append(df)
            data2 = pd.concat(df_list, axis=0).reset_index(drop=True)
            data2['cellLine'] = self._cell_line
            data2['runID'] = self._exp_id
            data2 = data2[['cellLine', 'runID', 'runTime', 'species', 'value', 'profile', 'kind', 'method']]
            data = pd.concat([data, data2], axis=0)

        return data'''

    '''@property
    def get_pre_process(self):
        ''''''
        species = self._spc_dict.copy()
        cell = species.pop('cell'.upper())
        product = species.pop('product'.upper())
        oxygen = species.pop('oxygen'.upper())

    # Get In Process DF
    @property
    def get_in_process(self):
        ''''''
        self._in_process = pd.concat([self._process_data_dict['prepro'],
                                      self._cell.get_ivcc(),
                                      self._cell.get_cumulative(),
                                      self._oxygen.get_cumulative(),
                                      self._product.get_cumulative(),
                                      self._process_data_dict['inpro']],
                                      axis=1)
        return self._in_process'''
    
    # Get Poly. Reg. Order DF
    def get_polyreg_order_df(self):
        return self._polyorder_df

    # Get Pre Process DF
    def get_pre_process(self):
        return self._pre_process

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