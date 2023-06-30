import pandas as pd
import numpy as np

from CCDPApy.in_process.GetterMixin import GetterMixin

###########################################################################
# Cell Mixin
###########################################################################
class CellMixin(GetterMixin):
    '''
    '''
    # Call methods
    def in_process(self):
        '''Caluculate in-process data for cell.
        '''
        ivcc = self.integral_viable_cell
        self._ixv = pd.Series(data=ivcc, name='ivcc_(x10^6_cells_hr/mL)')

        ccp = self.cumulative_cells_prod
        self._cumulative = pd.Series(data=ccp, name='cumCell_(x10^6_cells)')

        spr = self.sp_growth_rate
        self._sp_rate = pd.Series(data=spr, name='qCell_(1/hr)')
        # self._sp_growth_rate = self._sp_rate

        kd = self.kd
        self._kd = pd.Series(data=kd, name='kd')

        mv = self.mv
        self._mv = pd.Series(data=mv, name='mv')

    # Calculate Integral of Viable Cell
    @property
    def integral_viable_cell(self):
        idx = self._idx
        xv = self._xv.values[idx]           # Viable Cell Conc
        t = self._run_time_hour.values[idx] # Run Time (hours)

        # Initialize
        s = np.zeros(t.size)
        for i in range(1, len(t)):
            s[i] = s[i-1] + (xv[i] + xv[i-1]) / 2 * (t[i] - t[i-1])

        # Integral Of Viable Cell
        return s
        
    # Calculate Cumulative Cell Produced
    @property
    def cumulative_cells_prod(self):
        # Cells produced = xv(i) * v(i) - xv(i-1) * v(i-1)
        idx = self._idx
        xv = self._xv.values[idx]                   # vialbe cell concentration (10e6 cells/ml)
        v1 = self._v_before_sampling.values[idx]    # culture volume before sampling (ml)
        v2 = self._v_after_sampling.values[idx]     # culture volume after feeding (ml)

        # Initialize
        c = np.zeros(xv.size)
        c.fill(np.nan)
        c[0] = 0.0

        for i in range(1, len(idx)):
            c[i] = c[i-1] + xv[i] * v1[i] - xv[i-1] * v2[i-1]
        return c

    # Calculates Specific growth rate
    @property
    def sp_growth_rate(self):
        ''''''
        idx = self._idx
        t = self._run_time_hour.values[idx]         # run time (hrs)
        xv = self._xv.values[idx]                   # vialbe cell concentration (10e6 cells/ml)
        s = self._cumulative.values[idx]            # Cumulative Cell Concentraion (10e6 cells/mL)
        v1 = self._v_before_sampling.values[idx]    # Culture Volume Before Sampling (mL)
        v2 = self._v_after_sampling.values[idx]     # Culture Volume After Sampling (mL)

        # Initialize
        r = np.zeros(self._sample_num)
        r.fill(np.nan)
        for i in range(1, len(t)):
            x = s[i] - s[i-1]
            y = xv[i] * v1[i] + xv[i-1] * v2[i-1]
            r[i] = x / (y * 0.5 * (t[i] - t[i-1]))
        return r

    # Calculates kd value
    @property
    def kd(self):
        idx = self._idx
        xv = self._xv.values[idx]                   # Vialbe cell concentration (10e6 cells/ml)
        xd = self._xd.values[idx]                   # Dead Cell Concentration (10e6 cells/mL)
        t = self._run_time_hour.values[idx]         # Run Time (hrs)
        v1 = self._v_before_sampling.values[idx]    # Culture Volume Before Sampling (mL)
        v2 = self._v_after_sampling.values[idx]     # Culture Volume After Sampling (mL)

        # Initialize
        kd = np.zeros(self._sample_num)
        kd.fill(np.nan)
        for i in range(1, len(idx)):
            x = xd[i] * v1[i] - xd[i-1] * v2[i-1]
            y = xv[i] * v1[i] + xv[i-1] * v2[i-1]
            kd[i] = x / (y * 0.5 * (t[i] - t[i-1]))

        return kd

    # Calculate mv
    @property
    def mv(self):
        r = self._sp_rate.values
        kd = self._kd.values
        return (r + kd)

    #############################- Getters -#############################
    # Get Integral of Viable Cells
    @property
    def get_ivcc(self):
        return self._ixv
    
    @property
    def get_kd(self):
        return self._kd

    @property
    def get_sp_growth_rate(self):
        return self._sp_rate

    @property
    def get_mv(self):
        return self._mv
    
    @property
    def get_in_process(self):
        '''Return the in-process data.
        '''
        if self._in_process_flag:
            t = self._run_time_hour
            xv = self._xv
            xd = self._xd
            xt = self._xt
            ixv = self._ixv
            ccp = self._cumulative
            via = self._viability
            spr = self._sp_rate
            kd = self._kd
            mv = self._mv
        return pd.concat([t, xv, xd, xt, ixv, ccp, via, spr, kd, mv], axis=1)
    
    @property
    def get_in_process_data(self):
        '''Return the in-process data.
        '''
        if self._in_process_flag:
            xv = self._xv
            xd = self._xd
            xt = self._xt
            ixv = self._ixv
            ccp = self._cumulative
            via = self._viability
            spr = self._sp_rate
            kd = self._kd
            mv = self._mv
            data = [xv, xd, xt, via, 
                    ixv, ccp, 
                    spr, kd, mv]
            profile = ['concentration', 'concentration', 'concentration', 'concentration',
                       'cumulative', 'cumulative',
                       'spRate', 'spRate', 'spRate']
            kind = ['viable', 'dead', 'total', 'viability', 
                    'integral', 'cumulative', 
                    'growthRate', 'kd', 'mv']
            method_list = [np.nan, np.nan, np.nan, np.nan,
                           'twoPoint', 'twoPoint',
                           'twoPoint', 'twoPoint', 'twoPoint']
            return self.get_profile_data(data_list=data,
                                         profile_list=profile,
                                         kind_list=kind, 
                                         method_list=method_list)
        
    # Display
    @property
    def disp_in_process(self):
        if self._in_process_flag:
            data = self.get_in_process
            print('\n************ Cell In Process Data ************')
            print(data)