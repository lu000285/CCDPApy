import numpy as np

def mid_point_production(t_day, t_hour, c) -> tuple:
    '''Calculate mid points of the run time and concentration.
    '''
    c_mid = np.zeros((len(c)-1))
    t_day_mid = np.zeros((len(t_day)-1))
    t_hour_mid = np.zeros((len(t_hour)-1))

    for i in range(len(t_hour)-1):
        c_mid[i] = 0.5 * (c[i] + c[i+1])
        t_day_mid[i] = 0.5 * (t_day[i] + t_day[i+1])
        t_hour_mid[i] = 0.5 * (t_hour[i] + t_hour[i+1])

    return t_day_mid, t_hour_mid, c_mid


def mid_point_conc(t_day, t_hour, c1, c2):
    '''Calculate mid points of the run time and concentration.
    Attributes
    ----------
        t_day: array
            array of run time (day).
        t_hour: array
            array of run time (hr).
        c1: array
            concentration after feeding at t (mM).
        c2: array
            concentration before feeding at t+1 (mM).
    '''
    c_mid = np.zeros((len(t_hour)-1))
    t_day_mid = np.zeros((len(t_day)-1))
    t_hour_mid = np.zeros((len(t_hour)-1))

    for i in range(len(t_hour)-1):
        c_mid[i] = 0.5 * (c1[i] + c2[i+1])
        t_day_mid[i] = 0.5 * (t_day[i] + t_day[i+1])
        t_hour_mid[i] = 0.5 * (t_hour[i] + t_hour[i+1])

    return t_day_mid, t_hour_mid, c_mid