
from cProfile import label
from turtle import color, title
import matplotlib.pyplot as plt
import numpy as np

from ..helper_func.helper_func import output_path

###########################################################################
class PlotMixin:
    '''
    Plot species profiles.
    '''
    def plot(self, spc_list, profile, method=None,
             viability=False, osmolality=False, 
             combined=False, two_yaxis=False,
             file_name=None):
        '''
        Plot profiles for species.

        Parameters
        ----------
            spc_list : str, list of str
                species name to plot
            profile : str, list of str
                profiles to plot
                pass 'all', 'conc', 'cumulative', 'sp rate'.
            method : str, list of str
                methods to plot SP. rate.
                pass 'all', 'twopt', 'polyreg', 'rollreg'
            fig : matplotlib.pyplot.figure
        '''
        # Make spcies names upper case
        if type(spc_list)==str:
            spc_list = [spc_list.upper()]
        elif type(spc_list)==list:
            spc_list = [s.upper() for s in spc_list]
        print(spc_list)

        # Profile
        profile_dict = check_profile(profile=profile)
        print(profile_dict)
        # Method    
        method_dict = check_method(method=method)
        print(method_dict)

        # ax key; (row, column, index)
        row = len(spc_list) if not combined else 1
        column = sum(profile_dict.values())
        index = 1
        ax_key = (row, column, index)
        # print(ax_key)

        # Cleate Fig
        fig = plt.figure(figsize=(8*column, 6*row)) # (col, row)
        #fig, axes = plt.subplots(row, column)
        plt.subplots_adjust(wspace=0.8, hspace=0.2)
        #fig.tight_layout(rect=[0,0,1,0.96])

        # Concentration curve
        if profile_dict['concentration'] and self._in_process_flag:
            fig = self._plot_conc(fig=fig, spc_list=spc_list, ax_key=ax_key,
                                  viability=viability, osmolality=osmolality,
                                  combined=combined, two_yaxis=two_yaxis)
            index += 1
            ax_key = (row, column, index)

        # Cumulative curve
        if profile_dict['cumulative'] and self._in_process_flag:
            fig = self._plot_cumulative(fig=fig, spc_list=spc_list, ax_key=ax_key,
                                        combined=combined, two_yaxis=two_yaxis)
            index += 1
            ax_key = (row, column, index)

        # SP. Rate curve
        if profile_dict['sp_rate']:
            if sum(method_dict.values()):
                fig = self._plot_sp_rate(fig=fig, spc_list=spc_list, ax_key=ax_key,
                                         method_dict=method_dict,
                                         combined=combined, two_yaxis=two_yaxis)
            else:
                print('Please pass at least one method argument.')

        return fig



    def _plot_conc(self, fig, spc_list, ax_key,
                   viability=False, osmolality=False, 
                   combined=False, two_yaxis=False):
        '''
        Plot the concentration profile for species.

        Parameters:
        ----------
            fig : matplotlib.pyplot.figure
            spc_list : list of str
                species name to plot
            ax_key : tupple
                (column, row, index)
        '''
        # Get ax_key; (column, row, index)
        row, col, idx = ax_key
        ax = None
        for spc_name in spc_list:
            title_name = ''
            if spc_name=='CELL':
                spc = self.get_cell()
                y = spc.get_xv()    # y: viable cell 
                unit = '(x106 cells/mL)'
                label = 'Viable Cell'
            elif spc_name=='OXYGEN':
                spc = self.get_oxygen()
                y = spc.get_oxygen_consumed()   # y: oxygen consumed'''
                label = 'Oxygen'
            elif  spc_name=='IGG' or spc_name=='PRODUCT':
                spc = self.get_igg()
                y = spc.get_product_conc()  # y: concentration
                label = 'IgG'
                unit = '(mg/L)'
            else:
                spc_dict = self.get_spc_dict()
                #spc_dict.update(self.get_special_spc_dict())
                spc = spc_dict[spc_name]
                y = spc.get_conc_before_feed() # y: concentration
                unit = '(mM)'
                label = f'{spc_name.capitalize()}'
        
            x = spc.get_time_hour() # x: time

            # Add ax
            if not combined:
                ax = fig.add_subplot(row, col, idx)
                idx += col
                title_name = spc_name.capitalize() + ' '
            elif not ax:
                ax = fig.add_subplot(row, col, idx)

            ax.scatter(x, y, label=label)
            ax.plot(x, y)

            ax.set_title(f'{title_name}Kinetic Curve', loc='left')
            ax.set_ylabel(f'Concentration {unit}')
            ax.set_xlabel('Time (hrs)')
            anc = 1.1 if viability else 1.05
            ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

            if spc_name=='CELL' and viability:
                color = 'tab:red'
                ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
                y_via = spc.get_viability()
                label = 'Viability'
                ax2.scatter(x, y_via, label=label, color=color, marker='*')
                ax2.plot(x, y_via, color=color)
                ax2.set_ylim([0, 100])
                ax2.set_ylabel(f'Viability (%)', color=color)
                ax2.legend(bbox_to_anchor=(1.1, 0.5), loc='upper left', borderaxespad=0)

            if osmolality:
                osm = spc.get_oscmolality()

            if combined:
                ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)

        return fig



    def _plot_cumulative(self, fig, spc_list, ax_key,
                         combined=False, two_yaxis=False):
        '''
        Plot the cumulative consumption/production profile for species.

        Parameters:
        ----------
            fig : matplotlib.pyplot.figure
            spc_list : list of str
                species name to plot
            ax_key : tupple
                (row, column, index)
        '''
        # Get ax_key; (column, row, index)
        row, col, idx = ax_key
        ax = None
        for spc_name in spc_list:
            title_name = spc_name.capitalize() + ' '
            if spc_name=='CELL':
                spc = self.get_cell()
                unit = '(x106 cells/mL)'
            elif spc_name=='OXYGEN':
                spc = self.get_oxygen()
                unit = '(mmol)'
            elif  spc_name=='IGG' or spc_name=='PRODUCT':
                spc = self.get_igg()
                unit = '(mg)'
            else:
                spc_dict = self.get_spc_dict()
                #spc_dict.update(self.get_special_spc_dict())
                spc = spc_dict[spc_name]
                unit = '(mmol)'
            
            y = spc.get_cumulative() # y: cumulative
            x = spc.get_time_hour()  # x: time

            # Add ax
            if not combined:
                ax = fig.add_subplot(row, col, idx)
                idx += col
                title_name = ''
            elif not ax:
                ax = fig.add_subplot(row, col, idx)
            label = f'{title_name}'

            ax.scatter(x, y, label=label)

            # Poly. Reg
            if self._polyreg_flag:
                order = spc.get_polyorder()
                label = f'{title_name}Poly. Reg. Fit.\nOrder: {order}'
                data_num = 100
                x2 = np.linspace(x.iat[0], x.iat[-1], data_num)
                y2 = spc.get_polyfit_cumulative()(x2)
                ax.plot(x2, y2, label=label)
            
            if combined:
                title = 'Cumulative Curve'
            else:
                title = f'{spc_name.capitalize()} Cumulative Curve'
            ax.set_title(title, loc='left')
            ax.set_ylabel(f'Cumulative {unit}')
            ax.set_xlabel('Time (hrs)')
            ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
            if combined:
                ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)

        return fig
        


    def _plot_sp_rate(self, fig, spc_list, ax_key, method_dict,
                      combined=False, two_yaxis=False):
        '''
        Plot SP. rate profile for species.

        Parameters:
        ----------
            fig : matplotlib.pyplot.figure
            spc_list : list of str
                species name to plot
            ax_key : tupple
                (row, column, index)
            method : str, list of str
        '''
        # Get ax_key; (column, row, index)
        row, col, idx = ax_key
        ax = None
        for spc_name in spc_list:
            title_name = spc_name.capitalize() + ' '
            if spc_name=='CELL':
                spc = self.get_cell()
                unit = 'mu (hr^-1) [mv-kd]'
            elif spc_name=='OXYGEN':
                spc = self.get_oxygen()
                unit = '(mmol/10^9cell/hr)'
            elif  spc_name=='IGG' or spc_name=='PRODUCT':
                spc = self.get_igg()
                spc_name = 'Antibody'
                unit = '(mg/10^9cell/hr)'
            else:
                spc_dict = self.get_spc_dict()
                #spc_dict.update(self.get_special_spc_dict())
                spc = spc_dict[spc_name]
                unit = '(mmol/10^9cell/hr)'
            # Add ax
            if not combined:
                ax = fig.add_subplot(row, col, idx)
                idx += col
                title_name = ''
            elif not ax:
                ax = fig.add_subplot(row, col, idx)
            
            x = spc.get_time_hour()  # x: time

            # two-pt. calc.
            if method_dict['twopt'] and self._twopt_flag:
                label = f'{title_name}Two-Point Calc.'
                y = spc.get_sp_rate(method='twopt') # y: SP. rate
                ax.scatter(x, y)
                ax.plot(x, y, label=label)

            # Poly. Reg.
            if method_dict['polyreg'] and self._polyreg_flag:
                order = spc.get_polyorder()
                label = f'{title_name}Poly. Reg. Fit.\nOrder: {order}'
                y = spc.get_sp_rate(method='polyreg') # y: SP. rate
                ax.scatter(x, y)
                ax.plot(x, y, label=label)

            # Roll. Reg.
            if method_dict['rollreg'] and self._rollreg_flag:
                y, order, window = spc.get_sp_rate(method='rollreg') # y: SP. rate
                x2 = spc.get_time_mid()
                label = f'{title_name}Roll. Reg. Fit.\nOrder: {order} Window: {window}'
                ax.scatter(x2, y)
                ax.plot(x2, y, label=label)

            if combined:
                title = 'SP. Rate'
            else:
                title = f'{spc_name.capitalize()} SP. Rate'
            ax.set_title(title, loc='left')
            ax.set_ylabel(f'SP. rate {unit}')
            ax.set_xlabel('Time (hrs)')
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
            ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

        return fig


def check_profile(profile):
    '''
    Check profiles to plot.

    Parameters:
    -----------
        profile : str, list of str
            profiles to plot
            pass 'all', 'conc', 'cumulative', 'sp rate'.
    Returns
    -------
        profile_dict : dictonary
            dictionary of profiles.
    '''
    profile_dict = {}
    profile_dict['concentration'] = False
    profile_dict['cumulative'] = False
    profile_dict['sp_rate'] = False

    if 'all' in profile:
        profile_dict['concentration'] = True
        profile_dict['cumulative'] = True
        profile_dict['sp_rate'] = True
    else:
        if 'conc' in profile:
            profile_dict['concentration'] = True
        if 'cumulative' in profile:
            profile_dict['cumulative'] = True
        if 'sp rate' in profile:
            profile_dict['sp_rate'] = True

    return profile_dict

def check_method(method):
    '''
    Check methods to plot SP rate.

    Parameters:
    -----------
        profile : str, list of str
            profiles to plot
            pass 'all', 'twopt', 'polyreg', 'rollreg'.
    Returns
    -------
        profile_dict : dictonary
            dictionary of profiles.
    '''
    method_dict = {}
    method_dict['twopt'] = False
    method_dict['polyreg'] = False
    method_dict['rollreg'] = False
    if not method:
        return method_dict
    if 'all' in method:
        method_dict['twopt'] = True
        method_dict['polyreg'] = True
        method_dict['rollreg'] = True
    else:
        if 'twopt' in method:
            method_dict['twopt'] = True
        if 'polyreg' in method:
            method_dict['polyreg'] = True
        if 'rollreg' in method:
            method_dict['rollreg'] = True
    return method_dict
    

    '''def plot_1(self, spc_list, method=['twopt'], combined=False, save_file_name=None):
        # Initialize
        twopt = False
        polyreg = False
        rollreg = False

        # Check Regression Method to Plot
        if ('all' in method):
            twopt = True
            polyreg = True
            rollreg = True
        if ('twopt' in method):
            twopt = True
        if ('polyreg' in method):
            polyreg = True
        if ('rollreg' in method):
            rollreg = True
        
        # Mutiple species on the same plot
        if (combined):
            fig = plt.figure(figsize=(8*3, 6))


        # Each plot for each species
        else:
            n = len(spc_list)
            fig = plt.figure(figsize=(8*3, 6*n))

            for i, name in enumerate(spc_list):
                fig = self._spc_dict[name.upper()].plot_one(twopt=twopt,
                                                        polyreg=polyreg,
                                                        rollreg=rollreg,
                                                        fig=fig,
                                                        column=n,
                                                        ax_idx=1+i*3)

                fig.suptitle(f'Profils for {self._experiment_id}', fontsize='xx-large')

        return fig


    # Plotting for ONE Species
    def plot_one(self, twopt, polyreg, rollreg,
             concentration=True, cumulative=True, sp_rate=True,     
             fig=None, column=1, ax_idx = 1, figsize=(8, 6), data_num=100, 
             save_file_name=None):
        
        # column: 
        # ax_idx: start ax
        
        polyreg_data_num = data_num # number of data for polynomial regression
        f1 = concentration # and self._concentration.any()
        f2 = cumulative # and self._cumulative.any()
        f3 = sp_rate # and self._sp_rate.any()
        factor = 3
        if (factor == False):
            return None

        w, h = figsize
        size = (w*factor, h)
        if (fig==None):
            fig = plt.figure(figsize=size)
        fig.tight_layout(rect=[0,0,1,0.96])

        x = self._run_time_hour[self._idx]  # x axis data
        x2 = np.linspace(x.iat[0], x.iat[-1], polyreg_data_num) # x data for polynomial regression
        
        # Concentration Profile
        ax = fig.add_subplot(column, factor, ax_idx) # add axis
        # Plot
        if (f1):
            y = self._conc_before_feed[self._idx] # y axis data
            # ax.scatter(x, y, label=(self._name))    # plot
            ax.scatter(x, y)

            ax.plot(x, y)
            ax.set_title(f'{self._name} Kinetic Curve', loc='left')
            ax.set_ylabel('Concentration (mM)')
            ax.set_xlabel('Time (hrs)')
            # ax.legend()
            ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

        ax_idx += 1 # add ax index

        # Cumulative Profile
        ax = fig.add_subplot(column, factor, ax_idx) # add axis
        # Plot
        if (f2):
            y = self._cumulative[self._idx]    # y axis data
            # ax.scatter(x, y, label=(self._name))    # plot
            ax.scatter(x, y)

            # Add Polynomial Regression Fit on the same graph
            if (polyreg):
                y2 = self._polyfit(x2)
                ax.plot(x2, y2, color='orange', label=('Poly. Fit. Order:' + str(self._polyorder)))

            ax.set_title(f'{self._name} Cumulative Curve', loc='left')
            ax.set_ylabel('Cumulative (mmol)')
            ax.set_xlabel('Time (hrs)')
            ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
            ax.legend()

        ax_idx += 1 # add ax index
        
        # SP profile
        ax = fig.add_subplot(column, factor, ax_idx) # add axis
        # Plot
        if (f3):
            if (twopt):
                # Two-Point Calc
                y = self._sp_rate    # y axis data
                y[0] = 0             # replave pd.NA to 0 for plot 
                y = y[self._idx]

                ax.scatter(x, y)
                # ax.plot(x, y, label=(self._name + '\nTwo-Point Calc.'))    # plot
                ax.plot(x, y, label=('Two-Point Calc.'))

            # Polynomial Regression
            if (polyreg and not self._polyreg_sp_rate.empty):
                y2 = self._polyreg_sp_rate  # y axis data
                y2[0] = 0                   # replave pd.NA to 0 for plot
                y2 = y2[self._idx]

                ax.scatter(x, y2, marker='*')
                ax.plot(x, y2, ls=':',
                        label=('Poly. Reg. Fit.\nOrder: ' + str(self._polyorder)))

            if(rollreg and not self._rollpolyreg_sp_rate.empty):
                # Rolling Polynomial Regression
                x_mid = self._run_time_mid
                y3 = self._rollpolyreg_sp_rate
                o = self._rollpolyreg_order
                w = self._rollpolyreg_window
                label = f'Rolling Poly. Reg. Fit. \nOrder: {o} Window: {w}'

                ax.scatter(x_mid, y3, marker='D')
                ax.plot(x_mid, y3, ls='--', label=label)

            ax.set_title(f'{self._name} SP. Rate', loc='left')
            ax.set_ylabel('SP. rate (mmol/109 cell/hr)')
            ax.set_xlabel('Time (hrs)')
            ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
            ax.legend()

        ax_idx += 1 # add ax index

        fig.suptitle(self._name + ' Profile', fontsize='xx-large')

        # Save
        if (save_file_name != None):
            file_path = output_path(save_file_name)
            print(f'{save_file_name} Saving...')
            fig.savefig(file_path)
            print(f'{save_file_name} Saved\n')
  
        return fig'''