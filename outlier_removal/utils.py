import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import os

def estimating_missing_measuremnts(df, runID_lst, cols_lst, scale_lst):
    """
    function to intrapolate/extrapolate missing measurements in dataframe
    df: input data frame
    runID_lst: unique experimental ID list
    scale_lst: list of scales of data to be processed
    
    Return: df, processed dataframe
    """
    for col_name in cols_lst:
        for seed_scale in scale_lst:
            for i, runID in enumerate(runID_lst):
                idx_lst = df[(df['ID']== runID)&(df['Cell Line']== seed_scale)].index.tolist()
                # linear intrapolation/extrapolation
                df.loc[idx_lst,col_name] =df[(df['ID']== runID)&(df['Cell Line']== seed_scale)][col_name].interpolate(fill_value="extrapolate",limit_direction="both")
    return df

def cumulative_calculation(s_cum, s_conc, s_vol_before_sampling, s_vol_after_sampling, s_conc_after_feeding = None, s_fvol = None, s_fconc = None, prod = False):
    """
    function to calculate the cumulative consumption/production of species

    Args:
    s_cum: initialized full time series of cumulative consumption/poduction
    s_conc: selected time series of species concentration
    s_vol_before_sampling: time series of reactor volume (before sampling)
    s_vol_after_sampling: time series of reactor volume (after sampling)
    s_conc_after_feeding: time series of species concentration after feeding. Default = None
    s_fvol = time series of species feeding volume
    s_fconc = time series of species feeding concentration
    prod = indicator for cumulative production (True) or cumulative consumption (False, default)

    Return:
    s_cum: time series of cumulative consumption/poduction
    """ 
    # create copy of s_cum series
    s_cum = s_cum.copy()
    # create the index list
    idx_lst = s_conc.index.tolist()


    # check if there is measruement of concentration after feeding
    if s_conc_after_feeding is None:
    
        # check if there is feeding information or not
        if s_fvol is None or s_fconc is None:
            s_fvol = np.zeros(len(s_cum))
            s_fconc = np.zeros(len(s_cum))

            # placeholder: need to raise error if both feeding information and concentration after feeding are missing

        # calculate the cumulative consumption (mmol)
        for i, idx in enumerate(idx_lst):
            if i == 0:
                s_cum[idx] = 0
            else:
                s_cum[idx] = s_cum[idx-1] + (s_conc[idx-1]*s_vol_after_sampling[idx-1] + s_fconc[idx-1]*s_fvol[idx-1] - s_conc[idx]*s_vol_before_sampling[idx])/1000
        # flip sign if cumulative production
        if prod:
            s_cum.loc[idx_lst] = -s_cum[idx_lst]

    else: # if there is measruement of concentration after feeding

        # calculate the cumulative consumption (mmol)
        for i, idx in enumerate(idx_lst):
            if i == 0:
                s_cum[idx] = 0
            else:
                s_cum[idx] = s_cum[idx-1] + ((s_conc_after_feeding[idx-1] - s_conc[idx])*s_vol_before_sampling[idx])/1000
        # flip sign if cumulative production
        if prod:
            s_cum.loc[idx_lst] = -s_cum[idx_lst]
        
    return s_cum

# remove outlier based on filter
# check the pandas rolling function. Incclude the same input arguments as the rolling so that people can use different win_type. Let's use "exponetial" as default
def outlier_removal_other_parameters(scale, measurement_name, runID, s, window = None, threshold = 2, plot_ind = False):
    """
    function to remove outliers based rolling z-score of time series of a measuresment
    Arg:
    scale: reactor scale
    measurement_name: measurement name
    runID: ID of the experimental run
    s: time series of data
    plot_ind: boolean deciding if plotting the before and after profiles or not

    Return:
    s: Processed time series
    """

    if window is None:
        window = math.ceil(len(s)/3)

    # get a copy of s
    s = s.copy()
    s_raw = s.copy()

    roll = s.rolling(window=window, min_periods=1, closed = 'neither', center=True, win_type='exponential')
    # roll = s.rolling(window=window, min_periods=1, closed = 'neither', center=True, win_type='gaussian').mean(std=s.mean()*0.1) #both
    avg = roll.mean()
    std = roll.std() #ddof=0
    z = s.sub(avg).div(std)   
    m = z.between(-threshold, threshold)
    # replace outlier points with rolling average
    s = s.where(m, avg)

    # replcate outlier points with nan and interpolate/extrapolate
    s = s.where(m, np.nan)
    s = s.interpolate(fill_value="extrapolate",limit_direction="both")
    # roll = s.rolling(window=window, min_periods=1, closed = 'neither', center=True, win_type='gaussian').mean(std=s.mean()*0.1) #both
    roll = s.rolling(window=window, min_periods=1, closed = 'neither', center=True, win_type='exponential') 
    avg = roll.mean()
    # s = s.where(m, avg)
    s = avg



    if plot_ind:
        # create folder to store the smoothed profiles
        try:
            os.mkdir("input_files/outliers_removal")
        except:
            pass

        # create folder to store the smoothed profiles
        try:
            os.mkdir(f"input_files/outliers_removal/{scale}")
        except:
            pass

        try:
            path = f"input_files/outliers_removal/{scale}/{measurement_name}"
            
            os.mkdir(path)
        except:
            pass

        # before and after plot
        s_raw.plot(label='original')
        s.plot(label='smoothed')
        s[~m].plot(label='corrected values', marker='o', ls='')
        s_raw[~m].plot(label='outlier', marker='o', ls='')

        plt.legend()
        plt.savefig(f"{path}/run_{runID}.png")
        plt.clf()

    return s
    
def outlier_removal_species(scale,species_name, runID, s_cum, s_conc, s_vol_before_sampling, s_vol_after_sampling, s_conc_after_feeding = None, feed_idx_lst = [], s_fvol = None, s_fconc = None, window = None, threshold = 2, always_consumption = False, plot_ind = False):
    """
    function to remove outliers based on rolling z-score of time series of delta cumulative consumption/production at specified window size
    Arg:
    scale: reactor scale
    species_name: species name
    runID: ID of the experimental run
    s_cum: time series of cumulative consumption/production of species
    s_conc: time series of concentration of species
    s_vol_before_sampling: time series of reactor volumne before sampling
    s_vol_after_sampling: time series of reactor volumne after sampling
    s_conc_after_feeding: time series of concentration after feeding of species
    feed_idx_lst: list of indices that have feedings
    s_fvol: time series of feed volumn
    s_fconc: time series of feed concentration
    window: moving window size (default = (len(s_cum)-1)/3)
    threshhold: z-score threshold (default = 3)
    always_consumption: True if the species is always consumed/produced
    plot_ind: boolean deciding if plotting the before and after profiles or not

    Return 
    s_conc: processed time series of concentration
    """
    # get a copy of s_con
    s_conc = s_conc.copy()
    s_conc_raw = s_conc.copy()
    # get a copy of s_cum
    s_cum = s_cum.copy()
    s_cum_raw = s_cum.copy()
    
    
    # remove gluconeogenesis (gluoce production) outlier
    if species_name == "glucose":
        s_cum, s_conc, outlier_idx_lst = remove_gluconeogenesis(s_cum, s_conc, s_vol_before_sampling, s_vol_after_sampling, s_conc_after_feeding, feed_idx_lst, s_fvol, s_fconc)

    # get time series of delta cumulative consumption/production
    delta_s_cum = delta_cumulative_values_calculation(s_cum)
    
    delta_s_cum_raw = delta_s_cum.copy()

    # outlier removal and get the smoothed delta_s_cum

    delta_s_cum, outlier_idx_lst_1st_order = outlier_detector_1st_order(delta_s_cum, window = window, threshold = threshold, always_consumption = always_consumption)
    
    idx_lst = s_conc.index.tolist()

    # restimate the concentration at the detected outlier indices
    for i, idx in enumerate(outlier_idx_lst_1st_order):
        # check if there is measruement of concentration after feeding
        if idx != s_cum.index.tolist()[0]:
            if s_conc_after_feeding is None:
                if idx not in feed_idx_lst:    
                    if idx == idx_lst[0]:
                        s_conc.loc[idx] = ((delta_s_cum[idx])*1000 + s_conc[idx+1]*s_vol_before_sampling[idx+1]-s_fconc[idx]*s_fvol[idx])/s_vol_after_sampling[idx]
                    elif idx == idx_lst[-1]:
                        s_conc.loc[idx] = ((-delta_s_cum[idx-1])*1000 + s_conc[idx-1]*s_vol_after_sampling[idx-1]+s_fconc[idx-1]*s_fvol[idx-1])/s_vol_before_sampling[idx]
                    else:
                        s_conc_tmp1 = ((delta_s_cum[idx])*1000 + s_conc[idx+1]*s_vol_before_sampling[idx+1]-s_fconc[idx]*s_fvol[idx])/s_vol_after_sampling[idx]
                        s_conc_tmp2 = ((-delta_s_cum[idx-1])*1000 + s_conc[idx-1]*s_vol_after_sampling[idx-1]+s_fconc[idx-1]*s_fvol[idx-1])/s_vol_before_sampling[idx]
                        s_conc.loc[idx] = (s_conc_tmp1+s_conc_tmp2)/2
                else:
                    s_conc.loc[idx] = ((-delta_s_cum[idx-1])*1000 + s_conc[idx-1]*s_vol_after_sampling[idx-1]+s_fconc[idx-1]*s_fvol[idx-1])/s_vol_before_sampling[idx]
            else:
                if idx not in feed_idx_lst:
                    if idx == idx_lst[0]:
                        s_conc.loc[idx] = ((delta_s_cum[idx])*1000 + s_conc[idx+1]*s_vol_before_sampling[idx+1]-s_conc_after_feeding[idx]*s_vol_before_sampling[idx+1]+s_conc[idx]*s_vol_after_sampling[idx])/s_vol_after_sampling[idx]
                    elif idx == idx_lst[-1]:
                        if idx in feed_idx_lst:
                            s_conc.loc[idx] = ((-delta_s_cum[idx-1])*1000 + s_conc_after_feeding[idx-1]*s_vol_before_sampling[idx])/s_vol_before_sampling[idx]
                        else:
                            s_conc.loc[idx] = ((-delta_s_cum[idx-1])*1000 + s_conc[idx-1]*s_vol_before_sampling[idx])/s_vol_before_sampling[idx]
                    else:
                        s_conc_tmp1 = ((delta_s_cum[idx])*1000 + s_conc[idx+1]*s_vol_before_sampling[idx+1]-s_conc_after_feeding[idx]*s_vol_before_sampling[idx+1]+s_conc[idx]*s_vol_after_sampling[idx])/s_vol_after_sampling[idx]
                        if idx-1 in feed_idx_lst:
                            s_conc_tmp2 = ((-delta_s_cum[idx-1])*1000 + s_conc_after_feeding[idx-1]*s_vol_before_sampling[idx])/s_vol_before_sampling[idx]
                        else:
                            s_conc_tmp2 = ((-delta_s_cum[idx-1])*1000 + s_conc[idx-1]*s_vol_before_sampling[idx])/s_vol_before_sampling[idx]
                        
                        s_conc.loc[idx] = (s_conc_tmp1+s_conc_tmp2)/2
                else:
                    if idx-1 in feed_idx_lst:
                        s_conc.loc[idx] = ((-delta_s_cum[idx-1])*1000 + s_conc_after_feeding[idx-1]*s_vol_before_sampling[idx])/s_vol_before_sampling[idx]                
                    else:
                        s_conc.loc[idx] = ((-delta_s_cum[idx-1])*1000 + s_conc[idx-1]*s_vol_before_sampling[idx])/s_vol_before_sampling[idx]


    # create folder to store the smoothed profiles
    try:
        os.mkdir("input_files/outliers_removal")
    except:
        pass
    try:
        os.mkdir(f"input_files/outliers_removal/{scale}")
    except:
        pass
    try:
        path = f"input_files/outliers_removal/{scale}/{species_name}"
        
        os.mkdir(path)
    except:
        pass

    # before and after plot
    s_conc_raw.plot(label='original')
    s_conc.plot(label='smoothed')
    if species_name == "glucose":
        s_conc[outlier_idx_lst+outlier_idx_lst_1st_order].plot(label='corrected values', marker='o', ls='')
        s_conc_raw[outlier_idx_lst+outlier_idx_lst_1st_order].plot(label='outlier', marker='o', ls='')
    else:
        s_conc[outlier_idx_lst_1st_order].plot(label='corrected values', marker='o', ls='')
        s_conc_raw[outlier_idx_lst_1st_order].plot(label='outlier', marker='o', ls='')
        
    s_conc[[i for i in s_conc_raw.index.tolist() if i in feed_idx_lst]].plot(label='feed', marker='o', ls='')
    plt.legend()
    plt.savefig(f"{path}/run_{runID}.png")
    plt.clf()
    
    # s_cum_raw.plot(label='original')
    # if species_name == "glucose":
    #     s_cum_raw[outlier_idx_lst].plot(label='outlier', marker='o', ls='')
    
    # s_cum.plot(label='smoothed')
    # plt.legend()
    # plt.savefig(f"{path}/run_{runID}_cum.png")
    # plt.clf()

    # delta_s_cum_raw.plot(label='original')
    # delta_s_cum_raw[outlier_idx_lst_1st_order].plot(label='outlier', marker='o', ls='')
    
    # delta_s_cum.plot(label='smoothed')
    # plt.legend()
    # plt.savefig(f"{path}/run_{runID}_delta_cum.png")
    # plt.clf()

    return s_conc
            

def remove_gluconeogenesis(s_cum, s_conc, s_vol_before_sampling, s_vol_after_sampling, s_conc_after_feeding, feed_idx_lst, s_fvol, s_fconc):
    """
    function to detect outliers that show abnormal gluoconeogenesis from the time series of glucose cumulative consumption
    Arg:
    s_cum: time series of cumulative consumption/production of species
    s_conc: time series of concentration of species
    s_vol_before_sampling: time series of reactor volumne before sampling
    s_vol_after_sampling: time series of reactor volumne after sampling
    s_conc_after_feeding: time series of concentration after feeding of species
    feed_idx_lst: list of indices that have feedings
    s_fvol: time series of feed volumn
    s_fconc: time series of feed concentration
    
    Return:
    idx_lst: list of detected outlier indices
    """
    # get a copy
    s_cum = s_cum.copy()
    s_conc_raw = s_conc.copy()
    
    # get index list
    idx_lst = s_conc.index.tolist()

    # check if always_consumption
    outliers_idx_1st_lst = []
    outliers_idx_2nd_lst = []
    for i, idx in enumerate(s_cum.index.tolist()):
        if i != 0:
            if s_cum[idx] - s_cum[idx-1] < 0:
                if i ==1:
                    s_conc.loc[idx-1] = np.nan
                    avg = s_conc.rolling(window=6, min_periods=1, closed = 'both', center=True, win_type='exponential').mean()
                    s_conc.loc[idx-1] = avg[idx-1]
                    # s_conc.loc[idx-1] = s_conc_raw[idx] + np.random.uniform(0.5,1.0)
                else:
                    outliers_idx_2nd_lst.append(idx)
                    outliers_idx_1st_lst.append(idx-1)
    for i in outliers_idx_1st_lst:
        s_cum[i] = np.nan
    for i in outliers_idx_2nd_lst:
        s_cum[i] = np.nan

    # get the outlier indices
    outlier_idx_lst = s_cum[s_cum.isna()].index.tolist()
    
    # avg = s_conc.rolling(window=6, min_periods=1, closed = 'both', center=True, win_type='exponential').mean()
    # s_conc = s_conc.where(~s_conc.isna(), avg)

    # avg = s_cum.rolling(window=6, min_periods=1, closed = 'both', center=True, win_type='exponential').mean()
    # s_cum = s_cum.where(~s_conc.isna(), avg)


    # linearly interpolate/extrapolate the NaN points
    s_cum = s_cum.interpolate(fill_value="extrapolate",limit_direction="both")
    for idx in outlier_idx_lst:
        if idx != s_cum.index.tolist()[0]:
            # check if there is measruement of concentration after feeding
            if s_conc_after_feeding is None:
                if idx == idx_lst[0]:
                    s_conc.loc[idx] = ((s_cum[idx+1] - s_cum[idx])*1000 + s_conc[idx+1]*s_vol_before_sampling[idx+1]-s_fconc[idx]*s_fvol[idx])/s_vol_after_sampling[idx]
                elif idx == idx_lst[-1]:
                    s_conc.loc[idx] = ((s_cum[idx-1] - s_cum[idx])*1000 + s_conc[idx-1]*s_vol_after_sampling[idx-1]+s_fconc[idx-1]*s_fvol[idx-1])/s_vol_before_sampling[idx]
                else:
                    s_conc_tmp1 = ((s_cum[idx+1] - s_cum[idx])*1000 + s_conc[idx+1]*s_vol_before_sampling[idx+1]-s_fconc[idx]*s_fvol[idx])/s_vol_after_sampling[idx]
                    s_conc_tmp2 = ((s_cum[idx-1] - s_cum[idx])*1000 + s_conc[idx-1]*s_vol_after_sampling[idx-1]+s_fconc[idx-1]*s_fvol[idx-1])/s_vol_before_sampling[idx]
                    s_conc.loc[idx] = (s_conc_tmp1+s_conc_tmp2)/2
            else:
                if idx == idx_lst[0]:
                    s_conc.loc[idx] = ((s_cum[idx+1] - s_cum[idx])*1000 + s_conc[idx+1]*s_vol_before_sampling[idx+1]-s_conc_after_feeding[idx]*s_vol_before_sampling[idx+1]+s_conc[idx]*s_vol_after_sampling[idx])/s_vol_after_sampling[idx]
                elif idx == idx_lst[-1]:
                    if idx in feed_idx_lst:
                        s_conc.loc[idx] = ((s_cum[idx-1] - s_cum[idx])*1000 + s_conc_after_feeding[idx-1]*s_vol_before_sampling[idx])/s_vol_before_sampling[idx]
                    else:
                        s_conc.loc[idx] = ((s_cum[idx-1] - s_cum[idx])*1000 + s_conc[idx-1]*s_vol_before_sampling[idx])/s_vol_before_sampling[idx]
                else:
                    
                    s_conc_tmp1 = ((s_cum[idx+1] - s_cum[idx])*1000 + s_conc[idx+1]*s_vol_before_sampling[idx+1]-s_conc_after_feeding[idx]*s_vol_before_sampling[idx+1]+s_conc[idx]*s_vol_after_sampling[idx])/s_vol_after_sampling[idx]
                    if idx-1 in feed_idx_lst:
                        s_conc_tmp2 = ((s_cum[idx-1] - s_cum[idx])*1000 + s_conc_after_feeding[idx-1]*s_vol_before_sampling[idx])/s_vol_before_sampling[idx]
                    else:
                        s_conc_tmp2 = ((s_cum[idx-1] - s_cum[idx])*1000 + s_conc[idx-1]*s_vol_before_sampling[idx])/s_vol_before_sampling[idx]

                    
                    s_conc.loc[idx] = (s_conc_tmp1+s_conc_tmp2)/2
        


    return s_cum, s_conc, outlier_idx_lst


def delta_cumulative_values_calculation(s_cum):
    """
    function to generate the time series of delta cumulative consumption/production, delta_s_cum[t] = s_cum[t+1] - s_cum[t]
    Arg:
    s_cum: time series of cumulative consumption/production

    Return:
    delta_s_cum: time series of delta cumulative consumption/production
    """
    # get the index list
    idx_lst = s_cum.index.tolist()[:-1]

    # initialize delta_s_cum series
    delta_s_cum = s_cum[idx_lst[:-1]].copy()

    # delta cumulative consumption/production calculate
    for i, idx in enumerate(idx_lst):
        delta_s_cum.loc[idx] = s_cum[idx+1] - s_cum[idx]

    return delta_s_cum

def outlier_detector_1st_order(delta_s_cum, window = None, threshold = 3, always_consumption = False):
    """
    function to detect outliers from the time series of delta cumulative values (1st order)
    Arg:
    delta_s_cum: time series of delta cumulative consumption/production, delta_s_cum[t] = s_cum[t+1] - s_cum[t]
    window: moving window size (default = (len(s_cum)-1)/3) for outlier detection using rolling average z-score
    threshhold: z-score threshold (default = 3)
    always_consumption: True if the species should always get consumed (like glucose)

    Return:
    outlier_idx_lst: list of detected outlier indices
    delta_s_cum: processed time series
    """
    delta_s_cum = delta_s_cum.copy()
    if window is None:
        window = math.ceil(len(delta_s_cum)/3)

    if always_consumption:
        delta_s_cum = delta_s_cum.where(delta_s_cum > 0, np.nan) 
    
    roll = delta_s_cum.rolling(window=window, min_periods=1, closed = 'both', center=True, win_type='exponential')
    avg = roll.mean()
    std = roll.std() #ddof=0
    # avg = delta_s_cum.rolling(window=window, min_periods=1, closed = 'neither', center=True, win_type='gaussian').mean(std=delta_s_cum.mean()*0.001) #both
    # std = delta_s_cum.rolling(window=window, min_periods=1, closed = 'neither', center=True, win_type='gaussian').std(std=delta_s_cum.mean()*0.001) #both
    # roll = delta_s_cum.rolling(window=window, min_periods=1, closed = 'neither', center=True, win_type='gaussian').mean(std=delta_s_cum.mean()*0.1) #both

    z = delta_s_cum.sub(avg).div(std)   
    m = z.between(-threshold, threshold)
    # replace outlier points with NaN 
    delta_s_cum = delta_s_cum.where(m, np.nan) 
    # store the list of detected outlier indices
    outlier_idx_lst = delta_s_cum[delta_s_cum.isna()].index.tolist()
    # interpolate/extrapolate the NaN points using cubicspline
    # delta_s_cum = delta_s_cum.interpolate(method='cubicspline',order=3,fill_value="extrapolate",limit_direction="both")
    delta_s_cum = delta_s_cum.interpolate(fill_value="extrapolate",limit_direction="both")
    # roll = delta_s_cum.rolling(window=window, min_periods=1, closed = 'both', center=True)
    roll = delta_s_cum.rolling(window=window, min_periods=1, closed = 'both', center=True, win_type='exponential')
    avg = roll.mean()
    # avg = delta_s_cum.rolling(window=window, min_periods=1, closed = 'neither', center=True, win_type='gaussian').mean(std=delta_s_cum.mean()*0.001) #both
    
    delta_s_cum = delta_s_cum.where(m, avg) 


    # include the adjacent points to be recalculated (mark as outliers as well)
    outlier_idx_lst_tmp = []
    for i in outlier_idx_lst:
        if i+1 not in outlier_idx_lst:
            if i+1!= delta_s_cum.index.tolist()[1]:
                outlier_idx_lst_tmp.append(i+1)
    outlier_idx_lst = outlier_idx_lst + outlier_idx_lst_tmp

    return delta_s_cum, outlier_idx_lst

