import pandas as pd

from .SPRateMixin import SPRateMixin
from .RatioCalcMixin import RatioCalcMixin

class RollRegMixin(SPRateMixin, RatioCalcMixin):
    '''
    Mixin class for BioProcess to calcuarate specific rates for species using rolling polynomial regression.

    Mehods
    ------
        rolling_regression
    '''
    def roll_regression(self, order=3, windows=6):
        '''
        Calculate SP. rate for species using rolling polynomial regression.

        Parameters
        ----------
            order : int, defalut=3, optional
                polynomial order for rolling polynomial regression.
            windows : int, default=6, optional
                data point size used for rolling polynomial regression.
        '''
        method = 'rollreg'

        # Cell Logistic Growth
        cell = self.get_cell()
        mu_calc_df = pd.concat([cell.get_time_mid().rename('CELL RUN TIME (HOURS)'),
                                cell.midcalc_growth_rate_calc()],
                                axis=1)
        cell.set_method_flag(method=method, flag=True)

        # Cell
        '''order = polyorder.loc['CELL'].iat[0]
        cell = bio_process.get_cell()
        cell.rolling_poly_regression(polyreg_order=3, windows = 4)'''

        # Oxygen
        '''order = polyorder.loc['OXYGEN'].iat[0]
        oxygen = bio_process.get_oxygen()
        oxygen.rolling_poly_regression(polyreg_order=3, windows = 4)'''

        # IgG
        '''order = polyorder.loc['IGG'].iat[0]
        igg = bio_process.get_igg()
        igg.rolling_poly_regression(polyreg_order=3, windows = 4)'''

        # Metabolite
        data_list = []  # df list to append data for each species

        for s in self._spc_list:
            data = pd.DataFrame()
            s = s.upper()   # Name
            spc = self._spc_dict[s.upper()]    # species object
            # calculate sp. rate
            spc.rolling_poly_regression(polyreg_order=order, windows=windows)
            # Set Flag True
            spc.set_method_flag(method=method, flag=True)
            
            q = spc.get_sp_rate(method=method)
            pre = f'Roll. Poly. Reg. Order: {order} Window: {windows}'
            title = f'{pre} q{s.capitalize()} (mmol/109 cell/hr)'

            name = self._name_dict[s.capitalize()]
            data[f'{name} RUN TIME (HOURS)'] = spc.get_time_mid() # run time 
            data[f'{name} CONC. MID. (mM)'] = spc.get_conc_mid() # concentraion
            data[title] = q # SP. rate
            data[f'r{name}']= q / 0.0016 # Residual

            # add data to data list
            data_list.append(data)

        # Add data for cell to data_list
        data_list.append(mu_calc_df)

        # Concat data_list
        rollreg_df = pd.concat(data_list, axis=1)

        # Set df to BioProcess
        self.set_process_data(process=method, data=rollreg_df)

        # SP. rate for Nitrogen and AA Carbon
        self.sp_rate_Nit_AAC(method=method)

        # Ratio Calc
        self.ratio_calc(method=method)

        # Set flag true
        self.set_process_flag(process=method, flag=True)

        print(self._process_data_dict[method])

    #*** End rolling_regression ***#