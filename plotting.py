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

plt.rcParams['font.family'] = 'Serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1
plt.rcParams["figure.autolayout"] = True
cm = 1/2.54  # centimeters in inches

powerOfFD = []
powerOfCPU = []
powerOfFEC = []
frequency = np.linspace(0, 100, 100)

for lines in frequency:
    powerOfFD.append(returnTotalComponentPower(component = 'FD', current_values=[lines, 4, 3/4, 2, 100, 30]))
    powerOfCPU.append(returnTotalComponentPower(component = 'CPU', current_values=[lines, 4, 3/4, 2, 100, 30]))
    powerOfFEC.append(returnTotalComponentPower(component = 'FEC', current_values=[lines, 4, 3/4, 2, 100, 30]))
    
fig = plt.figure(figsize = (15*cm, 7.5*cm))
plt.plot(frequency, powerOfFD, color=CB91_Blue)
plt.plot(frequency, powerOfCPU, color=CB91_Green)
plt.plot(frequency, powerOfFEC, color=CB91_Amber)