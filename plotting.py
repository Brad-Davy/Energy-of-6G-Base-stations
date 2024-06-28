#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 16:23:02 2024

@author: bradleydavy
"""

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
    fig = plt.figure(figsize=(15*cm, 7.5*cm))
    total_power = []

    for f in FREQUENCY_MAP:
        parameters = {'BW': f, 'Ant': 4, 'M': 3 /
                      4, 'R': 2, 'dt': 100, 'df': 100}
        total_power.append(np.sum(returnTotalPower(parameters)))

    total_power = np.array(total_power)

    plt.plot(FREQUENCY_MAP, total_power +
             calculateLeakagePower(total_power), color='black')
    plt.ylabel('Power / W')
    plt.xlabel('Frequency / MHz')
    plt.savefig('img/totalBaseBandPower.svg', dpi=500)


def reproduceFigure2():

    # =============================================================================
    # Paper data
    # =============================================================================
    load_frequency = np.array([0.0, 0.49, 0.90, 1.55, 2.36, 5.46, 9.54, 14.59,
                              21.60, 31.54, 36.92, 45.40, 56.97, 69.19, 79.79, 85.66, 93.48, 100.70])
    power_frequency = [398.8, 457.02, 490.23, 519.26, 531.66, 560.49, 601.70, 659.45,
                       729.51, 820.09, 865.35, 926.98, 1009.12, 1095.36, 1165.1, 1202.02, 1263.70, 1320.6]

    load_time = [0, 1.60, 7.78, 14.77, 21.96, 29.54, 36.73, 44.11,
                 50.80, 61.18, 71.56, 79.34, 89.32, 93.61, 97.50, 99.70]
    power_time = [97.27, 117.83, 194.94, 277.1, 369.72, 462.26,
                  549.66, 637.07, 719.32, 847, 976, 1074, 1192, 1243, 1295, 1320]

    interpolated_data = interp1d(load_frequency, power_frequency)
    LOAD = np.linspace(0, 0.99, 100)
    power_frequency_interpolated = [interpolated_data(i) for i in LOAD]

    total_power_PA = []
    total_power_BB = []
    total_power_RF = []
    total_power_Oh = []

    fig = plt.figure(figsize=(15*cm, 15*cm))

    # DEFAULT_BW = 10
    # DEFAULT_ANT = 2
    # DEFAULT_M = 6
    # DEFAULT_R = 5/6
    # DEFAULT_DT = 100
    # DEFAULT_DR = 100

    for l in LOAD:
        parameters = {'BW': 10, 'Ant': 4, 'M': 6, 'R': 5/6, 'dt': 1, 'df': l}
        BB, RF, PA, Oh = returnTotalPower(parameters)
        total_power_PA.append(PA)
        total_power_BB.append(BB)
        total_power_RF.append(RF)
        total_power_Oh.append(Oh)

    total_power_PA = np.array(total_power_PA)
    total_power_BB = np.array(total_power_BB)
    total_power_RF = np.array(total_power_RF)
    total_power_Oh = np.array(total_power_Oh)

    total_power_BB += calculateLeakagePower(np.array(total_power_BB))

    plt.plot(np.array(load_frequency) / 100, np.array(power_frequency),
             color='red', label='(Desset et al)')
    plt.plot(LOAD, total_power_PA, color=CB91_Green, label='Power amplifier')
    plt.plot(LOAD, total_power_BB, color=CB91_Blue, label='Baseband')
    plt.plot(LOAD, total_power_RF, color=CB91_Amber, label='Radio')
    plt.plot(LOAD, total_power_Oh, color=CB91_Violet, label='Overhead')
    plt.plot(LOAD, total_power_PA + total_power_BB + total_power_RF +
             total_power_Oh, color='black', linestyle='dotted', label='total')

    plt.ylabel('Power / W')
    plt.xlabel('Load / %')
    plt.legend()
    plt.savefig('img/totalBaseBandPower.svg', dpi=500)
    plt.show()


def determinePAHelper(target, BB, RF):
    PA = 0
    difference = 1
    while difference > 0:
        PA += 1
        newSum = BB + RF + PA + returnOverHead(BB, RF, PA)
        difference = target - newSum
    return PA


def determinePA():
    load_frequency = np.array([0.0, 0.49, 0.90, 1.55, 2.36, 5.46, 9.54, 14.59,
                              21.60, 31.54, 36.92, 45.40, 56.97, 69.19, 79.79, 85.66, 93.48, 100.70])
    power_frequency = [398.8, 457.02, 490.23, 519.26, 531.66, 560.49, 601.70, 659.45,
                       729.51, 820.09, 865.35, 926.98, 1009.12, 1095.36, 1165.1, 1202.02, 1263.70, 1320.6]

    interpolated_data = interp1d(load_frequency, power_frequency)  # targets
    PAlist = []
    for idx in np.linspace(0, 100, 100):
        target = interpolated_data(idx)
        df = idx / 100
        parameters = {'BW': 10, 'Ant': 4, 'M': 6, 'R': 5/6, 'dt': 1, 'df': df}
        BB, RF, PA, Oh = returnTotalPower(parameters)
        PA = determinePAHelper(target, BB, RF)
        PAlist.append(PA)
    return PAlist


reproduceFigure2()
parameters = {'BW': 25000, 'Ant': 8, 'M': 6, 'R': 5/6, 'dt': 1, 'df': 0.98}
baseBandPower, RFPower, PAPower, OHPower = returnTotalPower(parameters)
print((baseBandPower + RFPower + PAPower + OHPower) * 0.01)
