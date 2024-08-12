#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 16:23:02 2024

@author: bradleydavy
"""

from api import getPowerConsumption, getComponentPowerConsumption
from energyConsumption import *
import matplotlib.pyplot as plt
import numpy as np
from colours import *
from scipy.interpolate import interp1d


plt.rcParams['font.family'] = 'Serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1
plt.rcParams["figure.autolayout"] = True
cm = 1/2.54  # centimeters in inches

FREQUENCY_MAP = np.linspace(0, 100, 100)



def totalPowerBaseBand():
    fig = plt.figure(figsize = (15*cm, 7.5*cm))
    total_power = []

    for f in FREQUENCY_MAP:
        parameters = {'BW' : f, 'Ant' : 4, 'M' : 3/4, 'R' : 2, 'dt' : 99, 'df' : 99}
        total_power.append(getPowerConsumption(parameters)['power'])
        
    total_power = np.array(total_power)
    
    
    
    plt.plot(FREQUENCY_MAP, total_power + calculateLeakagePower(total_power), color='black')
    plt.ylabel('Power / W')
    plt.xlabel('Frequency / MHz')
    plt.savefig('img/totalBaseBandPower.svg', dpi=500)
    
    

def reproduceFigure2():
    
    # =============================================================================
    # Paper data    
    # =============================================================================
    load_frequency = np.array([0.0, 0.49, 0.90, 1.55, 2.36, 5.46, 9.54, 14.59, 21.60, 31.54, 36.92, 45.40, 56.97, 69.19, 79.79, 85.66, 93.48, 100.70])
    power_frequency = [398.8, 457.02, 490.23, 519.26, 531.66, 560.49, 601.70, 659.45, 729.51, 820.09, 865.35, 926.98, 1009.12, 1095.36, 1165.1, 1202.02, 1263.70, 1300.6]
    
    interpolated_data = interp1d(load_frequency, power_frequency)
    LOAD = range(0,99)
    power_frequency_interpolated = [interpolated_data(i) for i in LOAD]
    
    load_time = []
    power_time = []
    total_power_PA = []
    total_power_BB = []
    total_power_RF = []
    total_power_Oh = []
    
    fig = plt.figure(figsize = (15*cm, 15*cm))
    
    for l in LOAD:
        parameters = {'BW' : 10, 'Ant' : 4, 'M' : 3/4, 'R' : 2, 'dt' : l, 'df' : 100}
        componentPower = getComponentPowerConsumption(parameters)

        total_power_PA.append(componentPower['PA'])
        total_power_BB.append(componentPower['BB'])
        total_power_RF.append(componentPower['RF'])
        total_power_Oh.append(componentPower['Oh'])
        
    
    total_power_PA = np.array(total_power_PA)
    total_power_BB = np.array(total_power_BB)
    total_power_RF = np.array(total_power_RF)
    total_power_Oh = np.array(total_power_Oh)
    
    total_power_BB += calculateLeakagePower(np.array(total_power_BB))
    
    plt.plot(LOAD, total_power_PA, color = CB91_Green, label = 'Power amplifier')
    plt.plot(LOAD, total_power_BB, color = CB91_Blue, label = 'Baseband')
    plt.plot(LOAD, total_power_RF, color = CB91_Amber, label = 'Radio')
    plt.plot(LOAD, total_power_Oh, color = CB91_Violet, label = 'Overhead')
    plt.plot(LOAD, total_power_PA + total_power_BB + total_power_RF + total_power_Oh, color='black', linestyle = 'dotted', label = 'total')

    
    plt.plot(load_frequency, power_frequency, color = 'red', label = '(Desset et al)')
       
    plt.ylabel('Power / W')
    plt.xlabel('Load / %')
    plt.legend()
    plt.savefig('img/totalBaseBandPower.svg', dpi=500)
    plt.show()
    
totalPowerBaseBand()
reproduceFigure2()