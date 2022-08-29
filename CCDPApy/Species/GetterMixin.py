
class GetterMixin:
    '''
    '''
    def get_exp_id(self):
        """
        Get the experimant ID.
        """
        return self._experiment_id

    def get_cl_name(self):
        """
        Get the cell line name.
        """
        return self._cell_line_name

    def get_init_v(self):
        """
        Get initial culture volume.
        """
        return self._initial_volume

    def get_experimenter(self):
        """
        Get the experimenter name.
        """
        return self._experimenter_name

    def get_v_before_samp(self):
        """
        Get culture volume before sampling
        """
        return self._v_before_sampling

    def get_v_after_samp(self):
        """
        Get culture volume after sampling
        """
        return self._v_after_sampling

    def get_v_after_feed(self):
        """
        Get culture volume after feeding.
        """
        return self._v_after_feeding
        
    def get_time_hour(self):
        '''
        Get run time (hour).
        '''
        return self._run_time_hour

    def get_time_mid(self):
        '''
        Get middle points of run time (hour).
        '''
        return self._run_time_mid

    def get_name(self):
        """
        Get species name.
        """
        return self._name

    def get_cumulative(self):
        """
        Get cumulative consumption/production.
        """
        return self._cumulative

    def get_cumulative_unit(self):
        """
        Get cumulative consumption/production unit.
        (mmol) or (mM).
        """
        return self._cumulative_unit

    def get_sp_rate(self, method):
        """
        Get Get SP. Rate.

        Parameters
        ----------
            method : str
                The method used to calculate SP. rate.
                'towpt', 'polyreg', 'rollreg'.

        """
        if (method=='twopt'):
            return self._sp_rate
        elif (method=='polyreg'):
            return self._polyreg_sp_rate
        elif (method=='rollreg'):
            return (self._rollpolyreg_sp_rate, self._rollpolyreg_order, self._rollpolyreg_window)
        else:
            print('wrong method parameter.')
            return None

    def get_polyorder(self):
        '''
        Get the polynomial regression order.
        '''
        return self._polyorder

    def get_polyfit_cumulative(self):
        '''
        Get the np.polyfit for the cumulative consumption/production.
        '''
        return self._polyfit

    def get_polyreg_cumulative(self):
        '''
        Get 
        '''
        return self._polyreg_cumulative

