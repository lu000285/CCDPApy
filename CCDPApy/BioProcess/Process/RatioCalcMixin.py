
class RatioCalcMixin:
    '''
    Mix in class for TwoPtMixin, PolyRegMixin, RollRegMixin to calculate the ratio of specific rates for species.

    Mehods
    ------
        ratio_calc
    '''
    def ratio_calc(self, method):
        '''
        Calculate the ratios for SP. rate for specific species.
        qLac/qGlc, qO2/qGlc, qGln/qGlc, and qNH3/qGln.

        Parameters
        ----------
            method : str
                name of the regression method.
                use 'twopt', 'polyreg', 'rollreg'.
        '''
        df = self.get_process_data(method=method)
        title = get_title(method)

        # qGlc
        if 'Glucose'.upper() in self._spc_list:
            qGlc = self._spc_dict['Glucose'.upper()].get_sp_rate(method=method)

            # qLac/qGlc
            if 'Lactate'.upper() in self._spc_list:
                qLac = self._spc_dict['Lactate'.upper()].get_sp_rate(method=method)
                if len(qLac) == len(qGlc):
                    df[f'{title} DL/DG (mmol/mmol)'] = qLac / qGlc

            # qO2/qGlc
            qO2 = self._oxygen.get_sp_rate_md()
            if len(qO2) == len(qGlc):
                df[f'{title} qO2/qGlc (mmol/mmol)'] = qO2 / qGlc

            # qGln/qGlc
            if 'Glutamine'.upper() in self._spc_list:
                qGln = self._spc_dict['Glutamine'.upper()].get_sp_rate(method=method)
                if len(qGln) == len(qGlc):
                    df[f'{title} qGln/qGlc (mmol/mmol)'] = qGln / qGlc

        # qNH3/qGln
        if ('NH3' in self._spc_list and 'Glutamine'.upper() in self._spc_list):
            qNH3 = self._spc_dict['NH3'].get_sp_rate(method='twopt')
            qGln = self._spc_dict['Glutamine'.upper()].get_sp_rate(method=method)
            if len(qNH3) == len(qGln):
                df[f'{title} qNH3/qGln (mmol/mmol)'] = qNH3 / qGln

    #*** End __ratio_calc ***#


# Other Helper Functions
def get_title(method):
    '''
    Get the title of SP. rate based on regression method.

    Parameters
    ----------
        method : str
            name of the regression method.
            use 'twopt', 'polyreg', 'rollreg'.

    Returns
    -------
        titel : str
            title.
    '''
    title = ''
    if method == 'twopt':
        title = 'Two-Pt. Calc.'
    elif method == 'polyreg':
        title = 'Poly. Reg.'
    elif method == 'rollreg':
        title = 'Roll. Poly. Reg'
    return title