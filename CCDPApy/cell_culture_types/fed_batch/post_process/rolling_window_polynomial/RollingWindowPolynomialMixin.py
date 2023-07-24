import pandas as pd

class RollingWindowPolynomialMixin():
    ''''''
    def rolling_window_polynomial(self, degree=3, window=6):
        '''
        '''
        species = self.get_species('all')
        species_list = list(species.keys())

        sp_rate_df_list = []

        # Logistic growth rate for the cell.
        if 'cell' in species_list:
            name = 'cell'
            species_list.remove(name)
            cell = species[name]

            # calculate growth rate
            cell.midcalc_growth_rate_calc()

            # concat
            sp_rate = cell.growth_rate.copy()
            sp_rate_logistic = cell.growth_rate_logistic.copy()
            sp_rate_data = pd.concat([sp_rate, sp_rate_logistic], axis=0).reset_index(drop=True)
            sp_rate_data['ID'] = self.cell_line_id
            cell.growth_rate = sp_rate_data

        # Product/IgG and Metabolite
        for name in species_list:
            spc = species[name]

            # calculate sp. rate.
            spc.rolling_window_polynomial(degree=degree, windows=window)

            sp_rate_data = spc.sp_rate_rolling.copy()
            sp_rate_data['species'] = name.capitalize()
            sp_rate_df_list.append(sp_rate_data)
        
        # concat sp. rate for rolling polynomial
        sp_rate_rolling_df = pd.concat(sp_rate_df_list, axis=0, ignore_index=True)
        # stored sp. rate
        sp_rate = self.sp_rate

        # concat 
        sp_rate_data = pd.concat([sp_rate, sp_rate_rolling_df], axis=0, ignore_index=True)
        sp_rate_data['ID'] = self.cell_line_id
        
        # save
        self.sp_rate = sp_rate_data