import matplotlib.pyplot as plt
import numpy as np

from ..helper_func.helper_func import output_path

###########################################################################
class PlotMixin:
    # Plotting for ONE Species obj
    def plot(self, concentration=True, cumulative=True, sp_rate=True,
             polyreg=True, rolling=False,
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
            ax.scatter(x, y, label=(self._name))    # plot

            ax.plot(x, y)
            ax.set_title('Kinetic Curve', loc='left')
            ax.set_ylabel('Concentration (mM)')
            ax.set_xlabel('Time (hrs)')
            ax.legend()
            ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)

        ax_idx += 1 # add ax index

        # Cumulative Profile
        ax = fig.add_subplot(column, factor, ax_idx) # add axis
        # Plot
        if (f2):
            y = self._cumulative[self._idx]    # y axis data
            ax.scatter(x, y, label=(self._name))    # plot

            # Add Polynomial Regression Fit on the same graph
            if (self._polyreg_cumulative.any()):
                y2 = self._polyfit(x2)
                ax.plot(x2, y2, color='orange', label=('Poly. Fit. Order:' + str(self._polyorder)))

            ax.set_title('Cumulative Curve', loc='left')
            ax.set_ylabel('Cumulative ' + self._name + ' (mmol)')
            ax.set_xlabel('Time (hrs)')
            ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
            ax.legend()

        ax_idx += 1 # add ax index
        
        # SP profile
        ax = fig.add_subplot(column, factor, ax_idx) # add axis
        # Plot
        if (f3):
            # Two-Point Calc
            y = self._sp_rate    # y axis data
            y[0] = 0             # replave pd.NA to 0 for plot 
            y = y[self._idx]

            ax.scatter(x, y)
            ax.plot(x, y, label=(self._name + '\nTwo-Point Calc.'))    # plot

            # Polynomial Regression
            if (polyreg and not self._polyreg_sp_rate.empty):
                y2 = self._polyreg_sp_rate  # y axis data
                y2[0] = 0                   # replave pd.NA to 0 for plot
                y2 = y2[self._idx]

                ax.scatter(x, y2, marker='*')
                ax.plot(x, y2, ls=':',
                        label=('Poly. Reg. Fit.\nOrder: ' + str(self._polyorder)))

            if(rolling and not self._rollpolyreg_sp_rate.empty):
                # Rolling Polynomial Regression
                x = self._run_time_mid
                y3 = self._rollpolyreg_sp_rate
                o = self._rollpolyreg_order
                w = self._rollpolyreg_window
                label = f'Rolling Poly. Reg. Fit. \nOrder: {o} Window: {w}'

                ax.scatter(x, y3, marker='D')
                ax.plot(x, y3, ls='--', label=label)

            ax.set_title('SP. Rate', loc='left')
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
  
        return fig