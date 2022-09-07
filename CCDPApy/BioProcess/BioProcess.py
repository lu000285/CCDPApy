# Python Libraries
import pandas as pd

# My Libraries
from ..helper_func.helper_func import check_key

from .GetterMixin import GetterMixin
from .SetterMixin import SetterMixin
from .DispMixin import DispMixin
from .BioProcessMixin import BioProcessMixin
from ..plotting.PlotMixin import PlotMixin
from CCDPApy.MeasuredData.MeasuredData import MeasuredData
from ..Species.Cell import Cell
from ..Species.Oxygen import Oxygen
from ..Species.Product import Product
from ..Species.Metabolite import Metabolite
from ..BioProcess.Process.InProcessMixin import InProcessMixin
from ..BioProcess.Process.TwoPtMixin import TwoPtMixin
from ..BioProcess.Process.PolyRegMixin import PolyRegMixin
from ..BioProcess.Process.RollRegMixin import RollRegMixin

###########################################################################
# Cell Bioprocess Class
###########################################################################
class BioProcess(InProcessMixin,
                 TwoPtMixin,
                 PolyRegMixin,
                 RollRegMixin,
                 BioProcessMixin,
                 GetterMixin,
                 SetterMixin,
                 DispMixin,
                 PlotMixin):
    '''
    Store cellular bioprocess information.

    Attributes
    ----------
        file_name : str
        measurement_sheet : str default='Measuerd Data', optional
        feed_sheet : str, default='Separate Feed Info', optional
        spc_list : list of str, default=[], optional
        new_spc_list : list of str, default=[], optional
    '''
    def __init__(self, 
                 file_name, 
                 measurement_sheet='Measured Data',
                 feed_sheet='Separate Feed Info',
                 spc_list=[],
                 new_spc_list=[],
                 **kwargs):
        '''
        Store cellular bioprocess information.

        Parameters
        ----------
            file_name : str
                Excel file name of measured data.
                Please include extension, '.xlsx'
            measurement_sheet : str default='Measuerd Data', optional
                Excel sheet name of meaured data.
            feed_sheet : str, default='Separate Feed Info', optional
                Excel sheet name of separate feed information.
            spc_list : list of str, default=[], optional
                List of species name to be analyzed, which must be in the default spcies list.
                Upper, lower, or capitalized case can be uesd. If this is not specified,
                the following default species list is to be used.
                default_spc_list = ['Alanine',   'Arginine', 'Asparagine','Aspartate', 'Cystine', 'Glucose', 'Glutamine', 'Glutamate', 'Glycine', 'Histidine', 'Isoleucine', 'Lactate', 'Leucine', 'Lysine', 'Methionine', 'NH3', 'Phenylalanine', 'Proline', 'Serine', 'Threonine', 'Tryptophan', 'Tyrosine', 'Valine', 'Ethanolamine']
            new_spc_list : list of str, default=[], optional
                List of new species name to be analuzed, which is not listed in the original species list.
        '''

        # Create MeasuredDate object
        self._md = MeasuredData(file_name=file_name,
                                measurement_sheet=measurement_sheet,
                                feed_sheet=feed_sheet)

        # Pre Process (calculate run time and culture volume)
        self._md.run_time()
        self._md.culture_volume()              
        
        # Species Object
        self._cell = Cell(name='cell',
                          measured_data=self._md) # Cell
        self._oxygen = Oxygen(name='oxygen',
                              measured_data=self._md)  # Oxygen
        self._product = Product(name='IgG',
                                measured_data=self._md) # Product/IgG

        # default species list
        default_spc_list = ['Alanine',   'Arginine',      'Asparagine',
                            'Aspartate', 'Cystine',       'Glucose',
                            'Glutamine', 'Glutamate',     'Glycine',
                            'Histidine', 'Isoleucine',    'Lactate',
                            'Leucine',   'Lysine',        'Methionine',
                            'NH3',       'Phenylalanine', 'Proline',
                            'Serine',    'Threonine',     'Tryptophan',
                            'Tyrosine',  'Valine',        'Ethanolamine']
        self._name_dict = {'Alanine'   : 'ALA', 'Arginine'      : 'ARG', 'Asparagine'   : 'ASN',
                           'Aspartate' : 'ASP', 'Cystine'       : 'CYS', 'Glucose'      : 'GLC',
                           'Glutamine' : 'GLN', 'Glutamate'     : 'GLU', 'Glycine'      : 'GLY',
                           'Histidine' : 'HIS', 'Isoleucine'    : 'ILE', 'Lactate'      : 'LAC',
                           'Leucine'   : 'LEU', 'Lysine'        : 'LYS', 'Methionine'   : 'MET',
                           'Nh3'       : 'NH3', 'Phenylalanine' : 'PHE', 'Proline'      : 'PRO',
                           'Serine'    : 'SER', 'Threonine'     : 'THR', 'Tryptophan'   : 'TRP',
                           'Tyrosine'  : 'TYR', 'Valine'        : 'VAL', 'Ethanolamine' : 'ETN'}


        self._default_spc_list = [s.upper() for s in default_spc_list] # make name upper case

        # Check spcies list
        self._spc_list = check_spc_list(default=self._default_spc_list,
                                        spc_list=spc_list, 
                                        new_spc_list=new_spc_list)

        # Create Metabolite object from spcies list and add to spcies dictionary
        self._spc_dict = metabolite(spc_list=self._spc_list, measured_data=self._md)
        
        #self._spc_cum_df = pd.DataFrame()          # Species Cumulative DF
        self._spc_conc_df = pd.DataFrame()         # Species Concenrtation DF
        self._conc_after_feed_df = pd.DataFrame()  # Species Concentration After Feeding DF
        
        # Bioprocess data df
        self._process_data_dict = {'prepro'  : self._md.get_pre_data(),
                                   'inpro'   : pd.DataFrame(),
                                   'twopt'   : pd.DataFrame(),
                                   'polyreg' : pd.DataFrame(),
                                   'rollreg' : pd.DataFrame(),}

        # Flags to check if the process is done
        self._process_flag_dict = {'inpro'   : False,
                                   'twopt'   : False,
                                   'polyreg' : False,
                                   'rollreg' : False,}

        # Cell Line Name and Exp ID Column
        self._expID_col = pd.Series(data=[self._md.exp_id] * len(self._md.sample_num), name='Experiment ID')
        self._cl_col = pd.Series(data=[self._md.cell_line_name] * len(self._md.sample_num), name='Cell Line')


# End BioProcess class

def check_spc_list(default, spc_list, new_spc_list):
    '''
    Check and return user-defined species list.

    Parameters
    ----------
        default : list of str
            default species list.
        spc_list : list of str
            user-speciefied species list.
            must be subset of default species list.
        new_spc_list : list of str
            new spcies list.
            must NOT be subset of default species list.
    '''
    # Check user species list
    if spc_list:
        spc_list = [s.upper() for s in spc_list] # make name upper case
        # check if spc list is subset of default spc list.
        assert (set(spc_list) <= set(default)), 'spcies list must be subset of default list.'
    else:
        spc_list = default

    # Check new species
    if new_spc_list:
        new_spc_list = [s.upper() for s in new_spc_list]    # make name upper case
        # check if new spc list is NOT subset of default spc list.
        assert not (set(new_spc_list) <= set(default)), 'new spcies list must not be subset of default list.'
        spc_list += new_spc_list    # add new spc to spc list

    return spc_list

    
def metabolite(spc_list, measured_data):
    '''
    Create Metabolite objects and return the dictionary.

    Parameters
    ----------
        spc_list : list of str
        measured_data : python object
            MeasuredData object
    Returns
    -------
        spc_dict : python dictionary
            {name: Metabolite object}
    '''
    df = measured_data.data_df  # DataFrame of measured data
    spc_dict = {}

    for spc_name in spc_list:
        conc_before = check_key(df=df, key=f'{spc_name} CONC. (mM)')   # Concentration Before Feeding
        conc_after = check_key(df=df, key=f'{spc_name} CONC. (mM).1')  # Concentration After Feeding
        feed = check_key(df=df, key=f'FEED {spc_name} CONC. (mM)')     # Feed Concentration

        # Check Calculated Cumulative Concentration
        cumulative = check_key(df=df, key=f'CUM {spc_name} CONS. (mM)')
        if (not cumulative.any()):
            cumulative = check_key(df=df, key=f'CUM {spc_name} PROD. (mM)')

        # Metabolite Object
        spc = Metabolite(name=spc_name,
                         measured_data=measured_data,
                         conc_before_feed=conc_before,
                         conc_after_feed=conc_after,
                         feed_conc=feed,
                         cumulative=cumulative,
                         production=True if (spc_name=='LACTATE' or spc_name=='NH3') else False)

        spc_dict[spc_name] = spc
    
    return spc_dict