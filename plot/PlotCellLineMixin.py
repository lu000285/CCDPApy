from operator import le, truediv
from re import T
from statistics import median_high
from turtle import title
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from ..helper_func.helper_func import output_path
# Plot Function for Cell Line Class

class PlotMixin:

    # Plotting different cell lines on the same figure
    def plot(self, cell_line, aa_lst, method,
             file_name=None, exp_lst=None, legend=True,
             ):

        polyreg = False
        rollreg = False

        if 'all' in method:
            polyreg = True
            rollreg = True
        if 'polyreg' in method:
            polyreg = True
        if 'rollreg' in method:
            rollreg = True
 
        bp_dict = self._cell_line_dict[cell_line]

        if (not exp_lst):
            exp_lst = [exp_id for exp_id in bp_dict.keys()]
        print(f'Makeing a plot for {exp_lst}')
        if (legend):
            legend = 'auto'

        # bp_dict = dict((bp.get_exp_id(), bp) for bp in self._cell_line)

        fig, ax = plt.subplots(len(aa_lst), 3, figsize=(24, 8*len(aa_lst)))
        fig.tight_layout(rect=[0,0,1,0.96])
        plt.subplots_adjust(wspace=0.2, hspace=0.3)
        # fig.suptitle(f'Profiles for {exp_lst}', fontsize='xx-large')
        fig.suptitle(f'Profiles for {exp_lst}')

        for i, s in enumerate(aa_lst):
            inpro_df_lst = []
            cumulative_lst = []
            sp_rate_df_lst = []
            for exp in exp_lst:
                aa = bp_dict[exp].get_aa_dict()[s.upper()]
                inpro_df = aa.get_inpro_df()
                cumulative_df = aa.get_cumulative_df()
                sp_rate_df = aa.get_sp_rate_df(polyreg=polyreg, rollreg=rollreg)
                
                inpro_df_lst.append(inpro_df)
                cumulative_lst.append(cumulative_df)
                sp_rate_df_lst.append(sp_rate_df)
                            
            inpro = pd.concat(inpro_df_lst, axis=0, ignore_index=True).sort_values('RUN TIME (HOURS)')
            cumulative = pd.concat(cumulative_lst, axis=0, ignore_index=True).sort_values('RUN TIME (HOURS)')
            sp_rate = pd.concat(sp_rate_df_lst, axis=0, ignore_index=True).sort_values('RUN TIME (HOURS)')

            # Conentration
            set_ax = ax[i, 0] if len(aa_lst) != 1 else ax[0]
            sns.lineplot(ax=set_ax, data=inpro, x='RUN TIME (HOURS)', y=f'{s.upper()} CONC. (mM)',
                            hue="Experiment ID", hue_order=exp_lst,
                            # style='Experiment ID',
                            legend=legend)
            set_ax.set_title(f'{s.upper()} Kinetic Curve', loc='center')
            set_ax.set_ylabel('Concentration (mM)')
            set_ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

            # Cumulative Consumption/Production
            set_ax = ax[i, 1] if len(aa_lst) != 1 else ax[1]
            sns.scatterplot(ax=set_ax, data=inpro, x='RUN TIME (HOURS)', y=f'CUM {s.upper()} (mmol)',
                            hue="Experiment ID", hue_order=exp_lst,
                            style="Experiment ID",
                            legend=legend)
            sns.lineplot(ax=set_ax, data=cumulative, x='RUN TIME (HOURS)', y=f'CUM {s.upper()} (mmol)',
                            hue="Experiment ID", hue_order=exp_lst,
                            style='Method',
                            legend=legend)
            set_ax.set_title(f'{s.upper()} Cumulative Curve', loc='center')
            set_ax.set_ylabel('Cumulative (mmol)')
            set_ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

            # Sp. Rate.
            set_ax = ax[i, 2] if len(aa_lst) != 1 else ax[2]
            sns.lineplot(ax=set_ax, data=sp_rate, x='RUN TIME (HOURS)', y=f'q{s.upper()} (mmol/109 cell/hr)',
                            hue="Experiment ID", hue_order=exp_lst,
                            style='Method',
                            legend=legend)
            sns.set_theme(style="whitegrid")
            set_ax.set_title(f'{s.upper()} SP. Rate', loc='center')
            set_ax.set_ylabel('SP. rate (mmol/109 cell/hr)')
            set_ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

        if (file_name):
            if '.png' not in file_name:
                file_name += '.png'
            file_path = output_path(file_name=file_name)

            print(f'{file_name} Saving......')
            plt.savefig(file_path)
            print(f'{file_name} Saved')

        return fig



    def plot2(self, aa_list, compare_cell_line, method,
              file_name=None,
              cell_line_list=None, exp_list=None,
              legend=True):

        twopt=False
        polyreg=False
        rollreg=False

        if 'all' in method:
            twopt=True
            polyreg=True
            rollreg=True

        if 'twopt' in method:
            twopt=True
        if 'polyreg' in method:
            polyreg=True
        if 'rollreg' in method:
            rollreg=True

        fig, ax = plt.subplots(len(aa_list), 3, figsize=(24, 8*len(aa_list)))
        fig.tight_layout(rect=[0,0,1,0.96])
        plt.subplots_adjust(wspace=0.2, hspace=0.3)

        cl_list = []
        exp_list = []
        bp_dict = {}
        for cell_line, bio_process_dict in self._cell_line_dict.items():
            cl_list.append(cell_line)
            for exp_id, bp in bio_process_dict.items():
                bp_dict[exp_id] = bp
                exp_list.append(exp_id)

        hue = 'Cell Line'
        style = 'Experiment ID'

        for i, s in enumerate(aa_list):
            inpro_df_lst = []
            cumulative_lst = []
            sp_rate_df_lst = []
            for exp in exp_list:
                aa = bp_dict[exp].get_aa_dict()[s.upper()]
                inpro_df = aa.get_inpro_df()
                cumulative_df = aa.get_cumulative_df()
                sp_rate_df = aa.get_sp_rate_df(twopt, polyreg, rollreg)
                
                inpro_df_lst.append(inpro_df)
                cumulative_lst.append(cumulative_df)
                sp_rate_df_lst.append(sp_rate_df)
                            
            inpro = pd.concat(inpro_df_lst, axis=0, ignore_index=True)
            cumulative = pd.concat(cumulative_lst, axis=0, ignore_index=True)
            sp_rate = pd.concat(sp_rate_df_lst, axis=0, ignore_index=True)

            # Conentration
            set_ax = ax[i, 0] if len(aa_list) != 1 else ax[0]
            sns.lineplot(ax=set_ax, data=inpro, x='RUN TIME (HOURS)', y=f'{s.upper()} CONC. (mM)',
                            hue=hue, hue_order=cl_list,
                            style=style,
                            legend=legend)
            set_ax.set_title(f'{s.upper()} Kinetic Curve', loc='center')
            set_ax.set_ylabel('Concentration (mM)')
            set_ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

            # Cumulative Consumption/Production
            set_ax = ax[i, 1] if len(aa_list) != 1 else ax[1]
            sns.scatterplot(ax=set_ax, data=inpro, x='RUN TIME (HOURS)', y=f'CUM {s.upper()} (mmol)',
                            hue=hue, hue_order=cl_list,
                            style=style,
                            legend=False
                            )
            sns.lineplot(ax=set_ax, data=cumulative, x='RUN TIME (HOURS)', y=f'CUM {s.upper()} (mmol)',
                            hue=hue, hue_order=cl_list,
                            style=style,
                            legend=legend)
            set_ax.set_title(f'{s.upper()} Cumulative Curve', loc='center')
            set_ax.set_ylabel('Cumulative (mmol)')
            set_ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

            # Sp. Rate.
            set_ax = ax[i, 2] if len(aa_list) != 1 else ax[2]
            sns.lineplot(ax=set_ax, data=sp_rate, kind='line', x='RUN TIME (HOURS)', y=f'q{s.upper()} (mmol/109 cell/hr)',
                            #hue=hue if (compare_cell_line) else 'Experiment ID',
                            hue='Cell Line',
                            #hue_order=cl_list if (compare_cell_line) else exp_list,
                            style=style if (compare_cell_line) else 'Method',
                            legend=legend)
            sns.set_theme(style="whitegrid")
            set_ax.set_title(f'{s.upper()} SP. Rate', loc='center')
            set_ax.set_ylabel('SP. rate (mmol/109 cell/hr)')
            set_ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

        if (file_name):
            if '.png' not in file_name:
                file_name += '.png'
            file_path = output_path(file_name=file_name)

            print(f'{file_name} Saving......')
            plt.savefig(file_path)
            print(f'{file_name} Saved')

        return fig


