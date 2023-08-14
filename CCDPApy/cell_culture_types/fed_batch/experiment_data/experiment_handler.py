import numpy as np
import pandas as pd

from .GetterMixin import GetterMixin

from CCDPApy.experiment_data import ExperimentDataHandler
from CCDPApy.helper import create_value_unit_df, split_name_unit, create_col_indices, add_descriptive_column
from CCDPApy.cell_culture_types.fed_batch.species import Cell, Product, Metabolite
from CCDPApy.cell_culture_types.fed_batch.in_process import InProcessMixin as Inprocess

from CCDPApy.Constants.fed_batch.column_name import EXPERIMENT_DATA_COLUMN, CONC_BEFOROE_FEED_COLUMN, FEED_VOLUME_COLUMN
from CCDPApy.Constants import DATE_COLUMN, CELL_LINE_COLUMN, ID_COLUMN, INITIAL_VOLUME_COLUMN, SAMPLE_VOLUME_COLUMN, BASE_ADDED_COLUMN, FEED_MEDIA_ADDED_COLUMN, VOLUME_BEFORE_SAMPLE_COLUMN, VOLUME_AFTER_SAMPLE_COLUMN, VIABLE_CELL_COLUMN, DEAD_CELL_COLUMN, TOTAL_CELL_COLUMN, PRODUCT_COLUMN
from CCDPApy.Constants.perfusion.excel_columns import EXPERIMENT_DATA_COLUMN
from CCDPApy.Constants.fed_batch.dict_key import EXP_DATA_KEY, FEED_VOLUME_KEY, CONC_BEFORE_FEED_KEY, CONC_AFTER_FEED_KEY, MEASURED_CUM_CONC_KEY, FEED_CONC_KEY, POLY_DEG_KEY

from CCDPApy.cell_culture_types.fed_batch.post_process import PolynomialMixin as Polynomial
from CCDPApy.cell_culture_types.fed_batch.post_process import RollingWindowPolynomialMixin as RollingPolynomial

COLUMNS_TO_DROP = [DATE_COLUMN, CELL_LINE_COLUMN, ID_COLUMN]

class FedBatchExperimentHandler(ExperimentDataHandler, GetterMixin, Inprocess, Polynomial, RollingPolynomial):
    '''
    '''
    def __init__(self, cell_line_name, cell_line_id, data, use_feed_conc, use_conc_after_feed,) -> None:
        super().__init__(cell_line_name, cell_line_id, data=data, cell_culture_type='fed-batch')

        self._use_feed_conc = use_feed_conc
        self._use_conc_after_feed = use_conc_after_feed

        conc_before_feed_data = data[CONC_BEFORE_FEED_KEY].copy()
        conc_after_feed_data = data[CONC_AFTER_FEED_KEY].copy()
        measured_cumulative_conc_data = data[MEASURED_CUM_CONC_KEY].copy()
        feed_conc_data = data[FEED_CONC_KEY].copy()
        feed_volume_data = data[FEED_VOLUME_KEY].copy()
        feed_mask = (feed_conc_data[CELL_LINE_COLUMN]==cell_line_name) & (feed_conc_data[ID_COLUMN]==cell_line_id)
        
        polynomial_degree_data = data['polynomial_degree_data'].copy()
        polynomial_degree_mask = (polynomial_degree_data[CELL_LINE_COLUMN]==cell_line_name) & (polynomial_degree_data[ID_COLUMN]==cell_line_id)

        # work with separate feed volume
        df = self._measured_data
        feed_conc_data = feed_conc_data[feed_mask].copy().reset_index(drop=True)
        feed_volume_data = feed_volume_data[self._mask].copy().reset_index(drop=True)
        feed_volume_sum = feed_volume_data.fillna(0).sum(axis=1).values
        feed_media_added = df[FEED_MEDIA_ADDED_COLUMN].fillna(0).values

        feed_data = {}
        if feed_conc_data.size!=0:
            for name in feed_conc_data['Feed Name'].unique():
                mask = feed_conc_data['Feed Name']==name
                df = feed_conc_data[mask].copy().dropna(axis=1)
                df = df.drop(['Cell Line', 'ID', 'Feed Name'], axis=1)

                if name in feed_volume_data.columns:
                    feed_vol = feed_volume_data[name].values
                else:
                    feed_vol = feed_media_added

                for col in df.columns:
                    feed_data[col.replace(' (mM)', '')] = {
                        'feed_conc': df[col].iat[0],
                        'feed_vol': feed_vol
                    }
        else:
            feed_data = {'feed_conc': 0.0, 'feed_vol': feed_media_added}
        '''
        separate_feed_mask = (separate_feed_conc_data[CELL_LINE_COLUMN]==cell_line_name) & (separate_feed_conc_data[ID_COLUMN]==cell_line_id)
        separate_feed_conc_data = separate_feed_conc_data[separate_feed_mask].copy()
        separate_feed_conc_data.drop(COLUMNS_TO_DROP, axis=1, inplace=True)

        # if all values are NAN, drop that column
        for col in separate_feed_conc_data.columns:
            df = separate_feed_conc_data[col]
            if df.isna().all():
                separate_feed_conc_data.drop(col, axis=1, inplace=True)
        '''
        self._feed_volume_data = feed_volume_data.fillna(0)
        self._conc_before_feed_data = conc_before_feed_data[self._mask].copy().reset_index(drop=True)
        self._conc_after_feed_data = conc_after_feed_data[self._mask].copy().reset_index(drop=True)
        self._measured_cumulative_conc_data = measured_cumulative_conc_data[self._mask].copy().reset_index(drop=True)
        self._feed_data = feed_data
        self._feed_conc_data = feed_conc_data
        self._feed_volume_sum = feed_volume_sum
        self._polynomial_degree_data = polynomial_degree_data[polynomial_degree_mask]
        
        # work with other parameters
        df = self._measured_data
        self._initial_volume = df[INITIAL_VOLUME_COLUMN].iat[0]
        self._sample_volumne = df[SAMPLE_VOLUME_COLUMN].fillna(0).values
        self._base_added = df[BASE_ADDED_COLUMN].fillna(0).values
        self._feed_media_added = feed_media_added
        
        self._viable_cell_conc = create_value_unit_df(df[VIABLE_CELL_COLUMN])
        self._dead_cell_conc = create_value_unit_df(df[DEAD_CELL_COLUMN])
        self._total_cell_conc = create_value_unit_df(df[TOTAL_CELL_COLUMN])
        self._product_conc = create_value_unit_df(df[PRODUCT_COLUMN])
        
        # pre-processing
        self._preprocess()

        # work with species object
        self._create_species()

        # work with cell concentration
        run_time = self._run_time
        cell = self.get_species('cell')
        vcd = cell.viable_cell_conc
        vcd['state'] = 'VCD'
        vcd = pd.concat([run_time, vcd], axis=1)

        tcd = cell.total_cell_conc
        tcd['state'] = 'TCD'
        tcd = pd.concat([run_time, tcd], axis=1)

        dcd = cell.dead_cell_conc
        dcd['state'] = 'DCD'
        dcd = pd.concat([run_time, dcd], axis=1)

        viab = cell.viability
        viab['state'] = 'Viability'
        viab = pd.concat([run_time, viab], axis=1)

        cell_conc = pd.concat([vcd, tcd, dcd, viab], axis=0).reset_index(drop=True)
        cell_conc['ID'] = self.cell_line_id
        self._cell_conc = cell_conc

        # variable to store processed data
        df.insert(df.shape[1]-1, "Viability (%)", viab['value'])

        # add run time df
        self._measured_data = pd.concat([df, self._run_time], axis=1)

        # Processed data
        exp_data = add_descriptive_column(self.get_measured_data(), EXPERIMENT_DATA_COLUMN)
        conc_before_feed = add_descriptive_column(self.get_conc_before_feed(), CONC_BEFOROE_FEED_COLUMN)
        self._processed_data = pd.concat([exp_data, conc_before_feed], axis=1)
        

    def _preprocess(self):
        '''data pre-processing.
        '''
        super()._preprocess()
        self._calculate_culture_volume()
        
    def _calculate_culture_volume(self):
        '''calculate culture volume before and after sampling.'''
        df = self._measured_data
        v_before_sample = df[VOLUME_BEFORE_SAMPLE_COLUMN]
        v_after_sample = df[VOLUME_AFTER_SAMPLE_COLUMN]

        # if no values in volume before and after sampling in measured data
        if v_before_sample.isna().all and v_after_sample.isna().all():
            init_v = self._initial_volume
            sample_v = self._sample_volumne
            base = self._base_added
            feed_media = self._feed_media_added
            feed_sum = self._feed_volume_sum
            n = sample_v.size

            # initialize
            v_before_sample = np.zeros(n)
            v_after_sample = np.zeros(n)
            v_after_feed = np.zeros(n)
            v_before_sample[0] = init_v

            # Added Supplements Volume; base + feed media + feed
            supplements_added = base + feed_media + feed_sum
            # supplements_added = base + feed_sum

            for i in range(n):
                # Volume After Sampling
                v_after_sample[i] = v_before_sample[i] - sample_v[i]
                            
                # Volume After Feeding
                v_after_feed[i] = v_after_sample[i] + supplements_added[i]
                
                # Volume Before Sampling
                if (i < n-1):
                    v_before_sample[i+1] = v_after_feed[i]
        
        else: 
            v_before_sample = v_before_sample.values
            v_after_sample = v_after_sample.values
        self._v_before_sample = v_before_sample
        self._v_after_sample = v_after_sample
        df[VOLUME_BEFORE_SAMPLE_COLUMN] = v_before_sample
        df[VOLUME_AFTER_SAMPLE_COLUMN] = v_after_sample

    def _create_species(self):
        '''crate specise object to analyze.'''
        spc_dict = {}
        run_time = self._run_time
        v_before_sample = self._v_before_sample
        v_after_sample = self._v_after_sample
        feed_media = self._feed_media_added
        viable_cell = self._viable_cell_conc
        dead_cell = self._dead_cell_conc
        total_cell = self._total_cell_conc
        production = self._product_conc
        conc_before_feed_df = self._conc_before_feed_data
        conc_after_feed_df = self._conc_after_feed_data
        feed_conc_df = self._feed_conc_data
        measured_cumulative_df = self._measured_cumulative_conc_data
        feed_data = self._feed_data
        feed_volume_sum = self._feed_volume_sum

        # if separate feed is empty, fill it with 0
        if feed_volume_sum.size==0:
            feed_volume_sum = np.zeros_like(run_time.shape[0])

        # Get indices
        conc_before_feed_indices = create_col_indices(conc_before_feed_df)
        conc_after_feed_indices = create_col_indices(conc_after_feed_df)
        feed_conc_indices = create_col_indices(feed_conc_df)
        measured_cumulative_indices = create_col_indices(measured_cumulative_df)

        cell = Cell(name='cell', run_time_df=run_time, volume_before_sampling=v_before_sample, volume_after_sampling=v_after_sample,
                    feed_media_added=feed_media, viable_cell_conc=viable_cell,
                    dead_cell_conc=dead_cell, total_cell_conc=total_cell)
        spc_dict['cell'] = cell

        name, _ = split_name_unit(production.index.name)
        product = Product(name=name, run_time_df=run_time, volume_before_sampling=v_before_sample,
                          volume_after_sampling=v_after_sample, feed_media_added=feed_media,
                          viable_cell_conc=viable_cell, production=production)
        spc_dict['product'] = product

        for name in conc_before_feed_indices.keys():
            if feed_conc_df.size==0:
                feed_conc = feed_data['feed_conc']
                feed_vol = feed_data['feed_vol']
            else:
                # Feeed conc.
                feed_conc = feed_data[name]['feed_conc']
                # Feed volume
                feed_vol = feed_data[name]['feed_vol']

            # Conc. before feeding
            index = conc_before_feed_indices[name]['index']
            data = conc_before_feed_df.iloc[:, index]
            conc_before_feed = create_value_unit_df(data)

            # Conc. after feeding
            index = conc_after_feed_indices[name]['index']
            data = conc_after_feed_df.iloc[:, index]
            conc_after_feed = create_value_unit_df(data)
            
            # Measured cumulative conc.
            index = measured_cumulative_indices[name]['index']
            data = measured_cumulative_df.iloc[:, index]
            measured_cumulative = create_value_unit_df(data)

            metabolite = Metabolite(name=name, run_time_df=run_time, volume_before_sampling=v_before_sample,
                                    volume_after_sampling=v_after_sample, feed_media_added=feed_media,
                                    viable_cell_conc=viable_cell, separate_feed_sum=feed_volume_sum, separate_feed=feed_vol,
                                    conc_before_feed=conc_before_feed, conc_after_feed=conc_after_feed, feed_conc=feed_conc,
                                    measured_cumulative_conc=measured_cumulative)
            spc_dict[name.lower()] = metabolite
            self._spc_dict = spc_dict
