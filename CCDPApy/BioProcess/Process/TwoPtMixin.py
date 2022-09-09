import pandas as pd

from .RatioCalcMixin import RatioCalcMixin

class TwoPtMixin(RatioCalcMixin):
    '''
    Mixin class for BioProcess to calculate specific rates for species using two-point calculations.

    Methods
    -------
        two_pt_calc
    '''

    def two_pt_calc(self):
        '''Calculate SP. rates for species using two-point calculations.
        '''
        method = 'twopt'

        # Cell
        self._cell.post_process_twopt() # Calculate sp. rate with two-point calc.
        self._cell.set_method_flag(method=method, flag=True)  # Set flag True

        # Oxygen
        self._oxygen.post_process_twopt() # Calculate sp. rate with two-point calc.
        self._oxygen.set_method_flag(method=method, flag=True)  # Set flag True

        # IgG/Product
        self._product.post_process_twopt()    # Calculate sp. rate with two-point calc.
        self._product.set_method_flag(method=method, flag=True)   # Set flag.

        # Metabolites
        data = self._process_data_dict[method]
        for s in self._spc_list:
            s = s.upper()   # Name
            spc = self._spc_dict[s] # Species object
            spc.sp_rate_twopt() # Calculate SP. rate
            spc.set_method_flag(method=method, flag=True)   # Set Flag True
            
            title = f'Two-Pt. Calc. q{s.capitalize()} (mmol/109 cell/hr)'
            data[title] = self._spc_dict[s].get_sp_rate(method='twopt')

        # SP. rates for Nitrogen and AA Carbon
        self.__sp_rate_Nit_AAC(method=method)

        # Ratio Calc.
        self.ratio_calc(method=method)

        # Set twopt Flag True
        self.set_process_flag(process=method, flag=True)

    #*** End two_pt_calc ***#

    #*** Private Methods ***#
    def __sp_rate_Nit_AAC(self, method):
        '''
        Calculate Specific Rates for Nitrogne and AA carbon.

        Parameters
        ----------
            method : str
                name of the regression method.
                use 'twopt'.
        '''
        # check default species list is a subset of species list of users
        if not (set(self._default_spc_list) <= set(self._spc_list)):
            return None

        # post process DataFrame
        df = self.get_process_data(method=method)

        qAla = self._spc_dict['Alanine'.upper()].get_sp_rate(method=method)
        qArg = self._spc_dict['Arginine'.upper()].get_sp_rate(method=method)
        qAsn = self._spc_dict['Asparagine'.upper()].get_sp_rate(method=method)
        qAsp = self._spc_dict['Aspartate'.upper()].get_sp_rate(method=method)
        qCys = self._spc_dict['Cystine'.upper()].get_sp_rate(method=method)
        qGln = self._spc_dict['Glutamine'.upper()].get_sp_rate(method=method)
        qGlu = self._spc_dict['Glutamate'.upper()].get_sp_rate(method=method)
        qGly = self._spc_dict['Glycine'.upper()].get_sp_rate(method=method)
        qHis = self._spc_dict['Histidine'.upper()].get_sp_rate(method=method)
        qIso = self._spc_dict['Isoleucine'.upper()].get_sp_rate(method=method)
        qLeu = self._spc_dict['Leucine'.upper()].get_sp_rate(method=method)
        qLys = self._spc_dict['Lysine'.upper()].get_sp_rate(method=method)
        qMet = self._spc_dict['Methionine'.upper()].get_sp_rate(method=method)
        qNh3 = self._spc_dict['Nh3'.upper()].get_sp_rate(method=method)
        qPhe = self._spc_dict['Phenylalanine'.upper()].get_sp_rate(method=method)
        qPro = self._spc_dict['Proline'.upper()].get_sp_rate(method=method)
        qSer = self._spc_dict['Serine'.upper()].get_sp_rate(method=method)
        qThr = self._spc_dict['Threonine'.upper()].get_sp_rate(method=method)
        qTry = self._spc_dict['Tryptophan'.upper()].get_sp_rate(method=method)
        qTyr = self._spc_dict['Tyrosine'.upper()].get_sp_rate(method=method)
        qVal = self._spc_dict['Valine'.upper()].get_sp_rate(method=method)

        # Check the length for data
        x = len(qAla) + len(qArg) + len(qAsn) + len(qAsp) + len(qCys)
        y = len(qGln) + len(qGlu) + len(qGly) + len(qHis) + len(qIso)
        z = len(qLeu) + len(qLys) + len(qMet) + len(qNh3) + len(qPhe)
        w = len(qPro) + len(qSer) + len(qThr) + len(qTry) + len(qTyr) + len(qVal)
        total_len = x + y + z + w
        if len(qAla) * 21 == total_len:

            # Nitrogen
            x = qAla*1 + qArg*4 + qAsn*2 + qAsp*1 + qCys*1
            y = qGln*2 + qGlu*1 + qGly*1 + qHis*3 + qIso*1
            z = qLeu*1 + qLys*2 + qMet*1 - qNh3   + qPhe*1
            w = qPro*1 + qSer*1 + qThr*1 + qTry*1 + qTyr*1 + qVal*1

            # Nitrogen SP. rate
            qNitrogen = (x + y + z + w).rename('qNitrogen (mmol/109 cells/hr)')

            # Nitrogen (w/o NH3, Ala) SP. rate
            qNitrogen_w_o_NH3_Ala = (qNitrogen - qAla + qNh3).rename('qNitrogen (w/o NH3, Ala) (mmol/109 cells/hr)')
            
            # Combine Nitrogen and Nitrogen (w/o NH3, Ala)
            nitrogen_rate = pd.concat([qNitrogen, qNitrogen_w_o_NH3_Ala], axis=1)

            # Add to spc dict
            self._spc_dict['NITROGEN'].set_sp_rate(nitrogen_rate)

            # Add to DF
            title = get_title(method)
            df[f'{title} qNitrogen (mmol/109 cells/hr)'] = qNitrogen
            df[f'{title} qNitrogen (w/o NH3, Ala) (mmol/109 cells/hr)'] = qNitrogen_w_o_NH3_Ala


        # Check the length for data
        x = len(qAla) + len(qArg) + len(qAsn) + len(qAsp) + len(qCys)
        y = len(qGln) + len(qGlu) + len(qGly) + len(qHis) + len(qIso)
        z = len(qLeu) + len(qLys) + len(qMet) + len(qPhe) + len(qPro)
        w = len(qSer) + len(qThr) + len(qTry) + len(qTyr) + len(qVal)
        total_len = x + y + z + w
        if len(qAla) * 20 == total_len:
            # aaC (mmol/109 cells/hr)
            x = qAla*3 + qArg*6 + qAsn*4 + qAsp*4 + qCys*6
            y = qGln*5 + qGlu*5 + qGly*2 + qHis*6 + qIso*6
            z = qLeu*6 + qLys*6 + qMet*5 + qPhe*9 + qPro*5
            w = qSer*3 + qThr*4 + qTry*4 + qTyr*9 + qVal*5

            # aaC SP. rate
            qaac = (x + y + z + w).rename('qaaC (mmol/109 cells/hr)')

            # aaC (consumption only) SP. rate
            x = qAla.abs()*3 + qArg.abs()*6 + qAsn.abs()*4 + qAsp.abs()*4 + qCys.abs()*6
            y = qGln.abs()*5 + qGlu.abs()*5 + qGly.abs()*2 + qHis.abs()*6 + qIso.abs()*6
            z = qLeu.abs()*6 + qLys.abs()*6 + qMet.abs()*5 + qPhe.abs()*9 + qPro.abs()*5
            w = qSer.abs()*3 + qThr.abs()*4 + qTry.abs()*4 + qTyr.abs()*9 + qVal.abs()*5
            qaac_cons = ((x + y + z + w + qaac) / 2).rename('qaaC (consumption only) (mmol/109 cells/hr)')

            # Combine aaC and aaC (consumption only)
            aac_rate = pd.concat([qaac, qaac_cons], axis=1)

            # Add to spc dict
            self._spc_dict['AA CARBON'].set_sp_rate(aac_rate)

            # Add to DF
            title = get_title(method)
            df[f'{title} qaaC (mmol/109 cells/hr)'] = qaac
            df[f'{title} qaaC (consumption only) (mmol/109 cells/hr)'] = qaac_cons

    #*** End __sp_rate_Nit_AAC ***#


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

