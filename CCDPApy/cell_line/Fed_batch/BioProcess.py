# Python Libraries
import pandas as pd

# My Libraries
from CCDPApy.helper import split_name_unit, create_col_indices, create_value_unit_df
from CCDPApy.MeasuredData import FedBatchMeasuredData as MeasuredData
from CCDPApy.constants import ExpInfoNamespace as Constants
from CCDPApy.Species.Fed_batch import Cell, Oxygen, Product, Metabolite
from CCDPApy.in_process.Fed_batch import InProcessMixin as Inprocess

from .GetterMixin import GetterMixin
#from BioProcessMixin import BioProcessMixin

from ..Process.PolyRegMixin import PolyRegMixin
from ..Process.RollRegMixin import RollRegMixin

class BioProcess(Inprocess, GetterMixin,
                 #PolyRegMixin, 
                 # RollRegMixin, 
                 #BioProcessMixin,
                 #SRatioMixin
                 ):
    '''
    Store cellular bioprocess information.

    Attributes
    ----------
        spc_list : list of str, default=[], optional
        new_spc_list : list of str, default=[], optional
    '''
    def __init__(self, data, use_feed_conc, use_conc_after_feed,
                 # spc_list=[], new_spc_list=[],
                 ):
        '''
        Store cellular bioprocess information.

        Parameters
        ----------
            spc_list : list of str, default=[], optional
                List of species name to be analyzed, which must be in the default spcies list.
                Upper, lower, or capitalized case can be uesd. If this is not specified,
                the following default species list is to be used.
                default_spc_list = ['Alanine',   'Arginine', 'Asparagine','Aspartate', 'Cystine', 'Glucose', 'Glutamine', 'Glutamate', 'Glycine', 'Histidine', 'Isoleucine', 'Lactate', 'Leucine', 'Lysine', 'Methionine', 'NH3', 'Phenylalanine', 'Proline', 'Serine', 'Threonine', 'Tryptophan', 'Tyrosine', 'Valine', 'Ethanolamine']
            new_spc_list : list of str, default=[], optional
                List of new species name to be analuzed, which is not listed in the original species list.
        '''
        key = Constants()

        # 
        self._use_feed_conc = use_feed_conc
        self._use_conc_after_feed = use_conc_after_feed

        # Create MeasuredDate object
        md = MeasuredData(data=data)
        
        # Experiment Information
        df = md.exp_info_df
        self._cell_line = md.cell_line
        self._exp_id = md.id
        self._initial_volume = md.initial_volume   

        # Make species list
        spc_list = []
        for col in md.conc_before_feed_df.columns:
            spc_list.append(split_name_unit(col)[0])
        # self._default_spc_name_dict = default_spc_name_dict
        # self._default_spc_list = [s.upper() for s in default_spc_list]
        # Check spcies list
        # self._spc_list = check_spc_list(default=self._default_spc_list, spc_list=spc_list,  new_spc_list=new_spc_list)

        # Create Metabolite object from spcies list and add to spcies dictionary
        spc_dict = create_metabolite(measured_data=md)
        cell = create_cell(measured_data=md)
        spc_dict['cell'] = cell
        product = create_product(measured_data=md)
        spc_dict['product'] = product

        self._spc_dict = spc_dict
        
        # List for Nitrogen, AA carbon
        self._spc_list_2 = []

        # Flags to check if the process is done
        self._process_flag_dict = {'inpro'   : False,
                                   'twopt'   : False,
                                   'polyreg' : False,
                                   'rollreg' : False,}
    

def create_cell(measured_data) -> Cell:
    sample_size = measured_data.sample_size
    run_time_day = measured_data.run_time_day
    run_time_hour = measured_data.run_time_hour
    volume_before_sampling = measured_data.volume_before_sampling
    volume_after_sampling = measured_data.volume_after_sampling
    feed_media_added = measured_data.feed_media_added
    viable_cell = measured_data.viable_cell_conc
    dead_cell = measured_data.dead_cell_conc
    total_cell = measured_data.total_cell_conc
    return Cell(name='cell', 
                samples=sample_size, 
                run_time_day=run_time_day, 
                run_time_hour=run_time_hour,
                volume_before_sampling=volume_before_sampling,
                volume_after_sampling=volume_after_sampling,
                feed_media_added=feed_media_added,
                viable_cell_conc=viable_cell,
                dead_cell_conc=dead_cell,
                total_cell_conc=total_cell)

def create_product(measured_data) -> Product:
    sample_size = measured_data.sample_size
    run_time_day = measured_data.run_time_day
    run_time_hour = measured_data.run_time_hour
    volume_before_sampling = measured_data.volume_before_sampling
    volume_after_sampling = measured_data.volume_after_sampling
    feed_media_added = measured_data.feed_media_added
    viable_cell = measured_data.viable_cell_conc
    production = measured_data.production
    index_name = production.index.name
    name, _ = split_name_unit(index_name)
    return Product(name=name, 
                   samples=sample_size, 
                   run_time_day=run_time_day, 
                   run_time_hour=run_time_hour,
                   volume_before_sampling=volume_before_sampling,
                   volume_after_sampling=volume_after_sampling,
                   feed_media_added=feed_media_added,
                   viable_cell_conc=viable_cell,
                   production=production)

def create_metabolite(measured_data) -> dict[str, Metabolite]:
    sample_size = measured_data.sample_size
    run_time_day = measured_data.run_time_day
    run_time_hour = measured_data.run_time_hour
    volume_before_sampling = measured_data.volume_before_sampling
    volume_after_sampling = measured_data.volume_after_sampling
    feed_media_added = measured_data.feed_media_added
    viable_cell = measured_data.viable_cell_conc
    separate_feed_df = measured_data.separate_feed_df
    conc_before_feed_df = measured_data.conc_before_feed_df
    conc_after_feed_df = measured_data.conc_after_feed_df
    feed_conc_df = measured_data.feed_conc_df
    measured_cumulative_df = measured_data.measured_cumulative_conc_df
    # Get indices
    separate_feed_indices = create_col_indices(separate_feed_df)
    conc_before_feed_indices = create_col_indices(conc_before_feed_df)
    conc_after_feed_indices = create_col_indices(conc_after_feed_df)
    feed_conc_indices = create_col_indices(feed_conc_df)
    measured_cumulative_indices = create_col_indices(measured_cumulative_df)

    # Create metabolite object
    spc_dict = {}
    for name in conc_before_feed_indices.keys():
        # Separate feed
        if separate_feed_indices.get(name):
            index = separate_feed_indices[name]['index']
            data = separate_feed_df.iloc[:, index]
            separate_feed = create_value_unit_df(data)
        else:
            separate_feed = None

        # Separate feed sum
        separate_feed_sum = separate_feed_df.fillna(0).sum(axis=1)
        
        # Conc. before feeding
        index = conc_before_feed_indices[name]['index']
        data = conc_before_feed_df.iloc[:, index]
        conc_before_feed = create_value_unit_df(data)

        # Conc. after feeding
        index = conc_after_feed_indices[name]['index']
        data = conc_after_feed_df.iloc[:, index]
        conc_after_feed = create_value_unit_df(data)
        
        # Feeed conc.
        index = feed_conc_indices[name]['index']
        data = feed_conc_df.iloc[:, index]
        feed_conc = create_value_unit_df(data)
        
        # Measured cumulative conc.
        index = measured_cumulative_indices[name]['index']
        data = measured_cumulative_df.iloc[:, index]
        measured_cumulative = create_value_unit_df(data)
        
        # Create object
        spc_dict[name.lower()] = Metabolite(name=name,
                                            samples=sample_size,
                                            run_time_day=run_time_day,
                                            run_time_hour=run_time_hour,
                                            volume_before_sampling=volume_before_sampling,
                                            volume_after_sampling=volume_after_sampling,
                                            feed_media_added=feed_media_added,
                                            viable_cell_conc=viable_cell,
                                            separate_feed=separate_feed,
                                            separate_feed_sum=separate_feed_sum,
                                            conc_before_feed=conc_before_feed,
                                            conc_after_feed=conc_after_feed,
                                            feed_conc=feed_conc,
                                            measured_cumulative_conc=measured_cumulative)
    return spc_dict




#####################################################################################################################
# Default Species list

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
    # Check user-defined species list
    if spc_list:
        spc_list = [s.upper() for s in spc_list] # make name upper case
        # check if spc list is subset of default spc list.
        assert (set(spc_list) <= set(default)), 'spcies list must be subset of default list.'
    else:
        spc_list = default

    # Check user-defined new species
    if new_spc_list:
        new_spc_list = [s.upper() for s in new_spc_list]    # make name upper case
        # check if new spc list is NOT subset of default spc list.
        assert not (set(new_spc_list) <= set(default)), 'new spcies list must not be subset of default list.'
        spc_list += new_spc_list    # add new spc to spc list

    return spc_list
