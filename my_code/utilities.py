import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import datetime
import os
#import network_calibration as nc


def get_value_at_index(array, indeces):
    """
    Returns the value of a time series at specified indices

    Parameters
    ----------
    array: 1d array of time series
    indeces: list of index to slice time series
    """
    local_val = np.empty(len(array))
    local_val.fill(np.nan)
    for i in indeces:
        local_val[i] = array[i]
    return local_val

def plot_epsilon_drawup_cds(cds_ts, local_min, local_max, epsilon_drawups, date_axis):
    min_val = get_value_at_index(list(cds_ts), local_min)
    max_val = get_value_at_index(list(cds_ts), local_max)
    epsilon_val = get_value_at_index(list(cds_ts), epsilon_drawups)
    print(date_axis)
    print(cds_ts)
    print(min_val)
    print(max_val)
    #start = datetime.datetime(2014, 5, 1)
    #end = datetime.datetime(2015, 3, 31)
    #date_axis = pd.bdate_range(start, end)
    #print(len(date_axis))
    #print()
    plt.plot(date_axis, cds_ts, linewidth=1)
    plt.plot(date_axis, min_val, '*', color='green')
    plt.plot(date_axis, max_val, '^', color='red')
    plt.plot(date_axis, epsilon_val, 'o', color='black')
    plt.grid('on')
    plt.title('Modified epsilon drawup')# for ' + entity_name, fontsize=20)
    plt.ylabel('CDS spread in bps', fontsize=20)
    #plt.xlabel('Date', fontsize=20)
    plt.rc('xtick', labelsize=15)
    plt.rc('ytick', labelsize=15)
    plt.legend(('CDS spread', 'Local minima', 'Local maxima',
                'Modified epsilon draw-up'), loc=2, prop={'size': 20})
    plt.show()




def plot_epsilon_drawup_entity(entities_np, entity_name, epsilon_choice, epsilon_down_time_parameter, epsilon_down_scale, minimal_epsilon_down, absolute_down,
                           epsilon_up_time_parameter, epsilon_up_scale, minimal_epsilon_up, absolute_up):
    """
    Plots the time seres of an entity together with local minima, local maxima and
    epsilon draw-up list

    Parameters
    ----------
    entities_np: 2d numpy matrix corresponding to time series of entities
    entity_name: string, name of the entity whose time series has to be plotted
    epsilon_choice: string parameter corresponding to standard deviation or percentage epsilon
    epsilon_time_parameter: int parameter corresponding to standard deviation calculation    

    """
    entity_index = np.where(entities_np[:, 0] == entity_name)
    entity_ts = np.ravel(entities_np[entity_index, 1:])
    #print entity_ts
    #print np.shape(entity_ts)
    #entity_ts = np.ravel(entities_np)
    print(np.shape(entity_ts))
    local_min_index, local_max_index = nc.compute_local_minmax(entity_ts)
    epsilon_drawup_list = nc.compute_epsilon_drawup(entity_ts, epsilon_choice, epsilon_down_time_parameter, epsilon_down_scale, minimal_epsilon_down, absolute_down,
                           epsilon_up_time_parameter, epsilon_up_scale, minimal_epsilon_up, absolute_up)

    print("epsilon= ", epsilon_drawup_list)
    local_min_val = get_value_at_index(entity_ts, local_min_index)
    local_max_val = get_value_at_index(entity_ts, local_max_index)
    #print local_min_index
    get_average_drawup(entity_ts,local_max_index,epsilon_drawup_list)
    epsilon_drawup_val = get_value_at_index(entity_ts, epsilon_drawup_list)
    #start = datetime.datetime(2014, 5, 1)
    #end = datetime.datetime(2015, 4, 15)

    start = datetime.datetime(2014, 5, 1)
    end = datetime.datetime(2015, 3, 31)
    date_axis = pd.bdate_range(start, end)
    print(len(date_axis))
    print()
    plt.plot(date_axis, entity_ts, linewidth=1)
    plt.plot(date_axis, local_min_val, '*', color='green')
    plt.plot(date_axis, local_max_val, '^', color='red')
    plt.plot(date_axis, epsilon_drawup_val, 'o', color='black')
    plt.grid('on')
    plt.title('Modified epsilon drawup for ' + entity_name, fontsize=20)
    plt.ylabel('CDS spread in bps', fontsize=20)
    #plt.xlabel('Date', fontsize=20)
    plt.rc('xtick', labelsize=15)
    plt.rc('ytick', labelsize=15)
    plt.legend(('CDS spread', 'Local minima', 'Local maxima',
                'Modified epsilon draw-up'), loc=2, prop={'size': 20})
    plt.show()