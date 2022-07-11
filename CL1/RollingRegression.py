import sys
import pandas as pd
import numpy as np
from pyrsistent import v
import scipy as sc
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import math
import types
import os
from pathlib import Path

#############################################################################################
############################## Rolling Polynomial Regression Functions ##############################
#############################################################################################

#############################################################################################
# Polynomial Regression
#############################################################################################
def rolling_poly_regression(self, polyreg_order=3, windows = 4):
    x = self._run_time
    y = self._cumulative
    vcc = self._vcc
    v = self._v_before
    x_mid = self._run_time_mid

    # Calculate Specific Rate from Derivetive of Polynomial Regression on Cumularive Consumption/Production
    q = pd.Series([np.nan] * (len(x)-1))

    # Calculate SP. rate
    for i in range(0, len(x_mid)):
        if i+1 < windows/2:
            x_roll = x[0:windows]
            y_roll = y[0:windows]
            # Polynomial Regression for Cumulative Consumption/Production
            fit = np.polyfit(x_roll, y_roll, polyreg_order)  # Fitting data to polynomial Regression (Get slopes)
            p = np.poly1d(fit)  # Get polynomial curve for Cumulative Consumption/Production

            dp1 = p.deriv()      # first derivetive of polynomial fit

            dy = dp1(x_mid[i])      # derivetive values corresponding to x
            q.iat[i] = dy / (vcc.iat[i] * v.iat[i]+vcc.iat[i+1] * v.iat[i+1])*2 * 1000
        elif i+windows/2 > len(x):
            x_roll = x[int(len(x)-windows/2-1):len(x)]
            y_roll = y[int(len(x)-windows/2-1):len(x)]
            # Polynomial Regression for Cumulative Consumption/Production
            fit = np.polyfit(x_roll, y_roll, polyreg_order)  # Fitting data to polynomial Regression (Get slopes)
            p = np.poly1d(fit)  # Get polynomial curve for Cumulative Consumption/Production

            dp1 = p.deriv()      # first derivetive of polynomial fit

            dy = dp1(x_mid[i])      # derivetive values corresponding to x
            q.iat[i] = dy / (vcc.iat[i] * v.iat[i]+vcc.iat[i+1] * v.iat[i+1])*2 * 1000
        else:
            x_roll = x[int(i-windows/2+1):int(i+windows/2+1)]
            y_roll = y[int(i-windows/2+1):int(i+windows/2+1)]
            # Polynomial Regression for Cumulative Consumption/Production
            fit = np.polyfit(x_roll, y_roll, polyreg_order)  # Fitting data to polynomial Regression (Get slopes)
            p = np.poly1d(fit)  # Get polynomial curve for Cumulative Consumption/Production

            dp1 = p.deriv()      # first derivetive of polynomial fit

            dy = dp1(x_mid[i])      # derivetive values corresponding to x
            q.iat[i] = dy / (vcc.iat[i] * v.iat[i]+vcc.iat[i+1] * v.iat[i+1])*2 * 1000

    self._rollpolyreg_sp_rate = q   # Polynomial Fit SP. rate

# Getters
def get_rollpolyreg_sp_rate(self):
    return self._rollpolyreg_sp_rate

# Ratio Caluculaions
def ratioCalcRollPolyReg(spc_dict):
    df = pd.DataFrame()
    
    # DL/DG
    dL = spc_dict['Lactate'].get_rollpolyreg_sp_rate()
    dG = spc_dict['Glucose'].get_rollpolyreg_sp_rate()
    df['DL/DG (mmol/mmol)'] = dL / dG

    # qO2/qGlc
    qO2 = spc_dict['Oxygen'].get_rollpolyreg_sp_rate()
    qGlc = dG
    df['qO2/qGlc (mmol/mmol)'] = qO2 / qGlc

    # qGln/qGlc
    qGln = spc_dict['Glutamine'].get_rollpolyreg_sp_rate()
    qGlc = dG
    df['qGln/qGlc (mmol/mmol)'] = qGln / qGlc

    # qNH3/qGln
    qNH3 = spc_dict['NH3'].get_rollpolyreg_sp_rate()
    qGln = qGln 
    df['qNH3/qGln (mmol/mmol)'] = qNH3 / qGln

    return df

# 
def RollPolynomialRegressionCalc(spc_dict,aa_lst,windows = 6):
    df = pd.DataFrame() # Initialize
    df['Run Time'] = spc_dict['Glucose'].get_run_time_mid()
    df_conc = pd.DataFrame() # Initialize
    df_q = pd.DataFrame() # Initialize
    df_r = pd.DataFrame() # Initialize
    r_lst = ['rglut1','rmct','rglnna','rasnna','raspna']
    # Calculate Polynomial Regression
    for  i,name in enumerate(['Glucose','Lactate','Glutamine','Asparagine','Aspartate']): #aa_lst:
        # order = 3
        if any(name == j for j in ['NH3','Oxygen','IgG']):
            continue
        else:
            spc = spc_dict[name.capitalize()]
        spc.rolling_poly_regression(windows = windows)
        unit = ' (mmol/10e9 cells/hr)'

        # Sp. Oxygen Consumption Rate
        df_q['q' + name +unit] = spc.get_rollpolyreg_sp_rate()
        df_conc['Conc. '+name+' (mM)'] = spc.get_conc_mid()
        df_r[r_lst[i]] = df_q['q' + name +unit]/0.0016
        # if name == 'Oxygen':
        #     spc.set_rollpolyreg_sp_OUR = types.MethodType(set_polyreg_sp_OUR, spc)
        #     ocr.mask(ocr <= 0, spc.get_rollpolyreg_sp_rate())
        #     spc.set_rollpolyreg_sp_OUR(ocr)
        #     df['SP. OUR (mmol/10e9 cells/hr)'] = spc.get_rollpolyreg_sp_rate()

        # # Change unit for IgG    
        # elif name == 'IgG':
        #     unit = ' (mg/10e9 cells/hr)'
        #     df['q' + name + unit] = spc.get_rollpolyreg_sp_rate()

        # else:
        #     df['q' + name +unit] = spc.get_rollpolyreg_sp_rate()
    # # Renameh
    # df.columns = ['Rolling Poly. Regression\n' + name for name in df.columns]
    # Ratio Calculation
    df_ratio = ratioCalcRollPolyReg(spc_dict)

    return pd.concat([df, df_conc, df_q, df_ratio,df_r], axis=1)


