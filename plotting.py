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

%matplotlib 

plt.rcParams['font.family'] = 'Serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1
plt.rcParams["figure.autolayout"] = True
cm = 1/2.54  # centimeters in inches

FREQUENCY_MAP = np.linspace(0, 100, 100)
LOAD = np.linspace(0,1,100)

def powerOfBasebandDownLink(total = False):   
    
    powerOfFD, powerOfCPU, powerOfFEC, powerOfFD_NL, powerOfOFDM, powerOfFILETER, powerOfDPD = returnBaseBandDowlinkEnergy(FREQUENCY_MAP)

    if total == False:
        fig = plt.figure(figsize = (15*cm, 7.5*cm))
        plt.ylabel('Power / W')
        plt.xlabel('Frequency / MHz')
        plt.plot(FREQUENCY_MAP, powerOfFD, color=CB91_Blue, label = 'FD')
        plt.plot(FREQUENCY_MAP, powerOfCPU, color=CB91_Green, label = 'CPU')
        plt.plot(FREQUENCY_MAP, powerOfFEC, color=CB91_Amber, label = 'FEC')
        plt.plot(FREQUENCY_MAP, powerOfFD_NL, color=CB91_Pink, label = 'FD (NL)')
        plt.plot(FREQUENCY_MAP, powerOfOFDM, color=CB91_Purple, label = 'OFDM')
        plt.plot(FREQUENCY_MAP, powerOfFILETER, color=CB91_Violet, label = 'Filter')
        plt.plot(FREQUENCY_MAP, powerOfDPD, color='gray', label = 'DPD')
        plt.legend(ncol = 3, frameon=False)
        plt.savefig('img/componentBaseBandPowerDownlink.svg', dpi=500)

    else:
        fig = plt.figure(figsize = (15*cm, 7.5*cm))
        plt.ylabel('Power / W')
        plt.xlabel('Frequency / MHz')
        total_power = np.array(powerOfFD) + np.array(powerOfCPU) + np.array(powerOfFEC) + np.array(powerOfFD_NL) + np.array(powerOfOFDM) + np.array(powerOfFILETER) + np.array(powerOfDPD)
        plt.plot(FREQUENCY_MAP, total_power + calculateLeakagePower(total_power), color='black')
        plt.savefig('img/totalBaseBandPowerDownlink.svg', dpi=500)
        
        
def powerOfBasebandUpLink(total = False):    
    
    powerOfFD, powerOfCPU, powerOfFEC, powerOfFD_NL, powerOfOFDM, powerOfFILETER = returnBaseBandUplinkEnergy(FREQUENCY_MAP)

    if total == False:
        fig = plt.figure(figsize = (15*cm, 7.5*cm))
        plt.ylabel('Power / W')
        plt.xlabel('Frequency / MHz')
        plt.plot(FREQUENCY_MAP, powerOfFD, color=CB91_Blue, label = 'FD')
        plt.plot(FREQUENCY_MAP, powerOfCPU, color=CB91_Green, label = 'CPU')
        plt.plot(FREQUENCY_MAP, powerOfFEC, color=CB91_Amber, label = 'FEC')
        plt.plot(FREQUENCY_MAP, powerOfFD_NL, color=CB91_Pink, label = 'FD (NL)')
        plt.plot(FREQUENCY_MAP, powerOfOFDM, color=CB91_Purple, label = 'OFDM')
        plt.plot(FREQUENCY_MAP, powerOfFILETER, color=CB91_Violet, label = 'Filter')
        plt.legend(ncol = 3, frameon=False)
        plt.savefig('img/componentBaseBandPowerUplink.svg', dpi=500)

    else:
        fig = plt.figure(figsize = (15*cm, 7.5*cm))
        plt.ylabel('Power / W')
        plt.xlabel('Frequency / MHz')
        total_power = np.array(powerOfFD) + np.array(powerOfCPU) + np.array(powerOfFEC) + np.array(powerOfFD_NL) + np.array(powerOfOFDM) + np.array(powerOfFILETER)
        plt.plot(FREQUENCY_MAP, total_power + calculateLeakagePower(total_power), color='black')
        plt.savefig('img/totalBaseBandPowerUplink.svg', dpi=500)
    
def totalPowerBaseBand():
    fig = plt.figure(figsize = (15*cm, 7.5*cm))
    powerOfFDUp, powerOfCPUUp, powerOfFECUp, powerOfFD_NLUp, powerOfOFDMUp, powerOfFILETERUp = returnBaseBandUplinkEnergy(FREQUENCY_MAP)
    powerOfFDDown, powerOfCPUDown, powerOfFECDown, powerOfFD_NLDown, powerOfOFDMDown, powerOfFILETERDown, powerOfDPDDown = returnBaseBandDowlinkEnergy(FREQUENCY_MAP)
    total_power_up = powerOfFDUp + powerOfCPUUp + powerOfFECUp + powerOfFD_NLUp + powerOfOFDMUp + powerOfFILETERUp 
    total_power_down = powerOfFDDown + powerOfCPUDown + powerOfFECDown + powerOfFD_NLDown + powerOfOFDMDown + powerOfFILETERDown + powerOfDPDDown 
    total_power = total_power_up + total_power_down
    plt.plot(FREQUENCY_MAP, total_power + calculateLeakagePower(total_power), color='black')
    plt.ylabel('Power / W')
    plt.xlabel('Frequency / MHz')
    plt.savefig('img/totalBaseBandPower.svg', dpi=500)
    
def powerOfRFTransmitter(total = False):    
    
    powerOfIQ, powerOfATTEN, powerOfBUFF, powerOfFVC, powerOfOFEVC, powerOfFM, powerOfCLK, powerOfDC, powerOfADC = returnRFTransmitterEnergy(FREQUENCY_MAP) 
   

    if total == False:
        fig = plt.figure(figsize = (15*cm, 7.5*cm))
        plt.ylabel('Power / W')
        plt.xlabel('Frequency / MHz')
        plt.plot(FREQUENCY_MAP, powerOfIQ / 1000, color=CB91_Blue, label = 'FD')
        plt.plot(FREQUENCY_MAP, powerOfATTEN / 1000, color=CB91_Green, label = 'CPU')
        plt.plot(FREQUENCY_MAP, powerOfBUFF/ 1000, color=CB91_Amber, label = 'FEC')
        plt.plot(FREQUENCY_MAP, powerOfFVC/ 1000, color=CB91_Pink, label = 'FD (NL)')
        plt.plot(FREQUENCY_MAP, powerOfOFEVC/ 1000, color=CB91_Purple, label = 'OFDM')
        plt.plot(FREQUENCY_MAP, powerOfFM/ 1000, color=CB91_Violet, label = 'Filter')
        plt.plot(FREQUENCY_MAP, powerOfCLK/ 1000, color='orange', label = 'Filter')
        plt.plot(FREQUENCY_MAP, powerOfDC/ 1000, color='orange', label = 'Filter')
        plt.plot(FREQUENCY_MAP, powerOfADC / 1000, color='orange', label = 'Filter')
        plt.legend(ncol = 3, frameon=False)
        plt.savefig('img/componentBaseBandPowerUplink.svg', dpi=500)

    else:
        fig = plt.figure(figsize = (15*cm, 7.5*cm))
        plt.ylabel('Power / W')
        plt.xlabel('Frequency / MHz')
        total_power = (np.array(powerOfIQ) + np.array(powerOfATTEN) + np.array(powerOfBUFF) + np.array(powerOfFVC) + np.array(powerOfOFEVC) + np.array(powerOfFM) + np.array(powerOfCLK) + np.array(powerOfDC) + np.array(powerOfADC)) / 1000
        plt.plot(FREQUENCY_MAP, total_power + calculateLeakagePower(total_power), color='black')
        plt.savefig('img/totalBaseBandPowerUplink.svg', dpi=500)






def powerOfRFReceiver(total = False):    
    
    powerOfIQ, powerOfATTEN, powerOfBUFF, powerOfFVC, powerOfOFEVC, powerOfFM, powerOfCLK, powerOfDC, powerOfADC = returnRFEnergy(FREQUENCY_MAP) 
   

    if total == False:
        fig = plt.figure(figsize = (15*cm, 7.5*cm))
        plt.ylabel('Power / W')
        plt.xlabel('Frequency / MHz')
        plt.plot(FREQUENCY_MAP, powerOfIQ / 1000, color=CB91_Blue, label = 'FD')
        plt.plot(FREQUENCY_MAP, powerOfATTEN / 1000, color=CB91_Green, label = 'CPU')
        plt.plot(FREQUENCY_MAP, powerOfBUFF/ 1000, color=CB91_Amber, label = 'FEC')
        plt.plot(FREQUENCY_MAP, powerOfFVC/ 1000, color=CB91_Pink, label = 'FD (NL)')
        plt.plot(FREQUENCY_MAP, powerOfOFEVC/ 1000, color=CB91_Purple, label = 'OFDM')
        plt.plot(FREQUENCY_MAP, powerOfFM/ 1000, color=CB91_Violet, label = 'Filter')
        plt.plot(FREQUENCY_MAP, powerOfCLK/ 1000, color='orange', label = 'Filter')
        plt.plot(FREQUENCY_MAP, powerOfDC/ 1000, color='orange', label = 'Filter')
        plt.plot(FREQUENCY_MAP, powerOfADC / 1000, color='orange', label = 'Filter')
        plt.legend(ncol = 3, frameon=False)
        plt.savefig('img/componentBaseBandPowerUplink.svg', dpi=500)

    else:
        fig = plt.figure(figsize = (15*cm, 7.5*cm))
        plt.ylabel('Power / W')
        plt.xlabel('Frequency / MHz')
        total_power = (np.array(powerOfIQ) + np.array(powerOfATTEN) + np.array(powerOfBUFF) + np.array(powerOfFVC) + np.array(powerOfOFEVC) + np.array(powerOfFM) + np.array(powerOfCLK) + np.array(powerOfDC) + np.array(powerOfADC)) / 1000
        plt.plot(FREQUENCY_MAP, total_power + calculateLeakagePower(total_power), color='black')
        plt.savefig('img/totalBaseBandPowerUplink.svg', dpi=500)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def reproduceFigure2():
    
    fig = plt.figure(figsize = (15*cm, 7.5*cm))
    
    powerOfFDUp, powerOfCPUUp, powerOfFECUp, powerOfFD_NLUp, powerOfOFDMUp, powerOfFILETERUp = returnFigure2EnergyUplink(LOAD)
    powerOfFDDown, powerOfCPUDown, powerOfFECDown, powerOfFD_NLDown, powerOfOFDMDown, powerOfFILETERDown, powerOfDPDDown = returnFigure2EnergyDownlink(LOAD)
   
    
    total_power_up = powerOfFDUp + powerOfCPUUp + powerOfFECUp + powerOfFD_NLUp + powerOfOFDMUp + powerOfFILETERUp 
    total_power_down = powerOfFDDown + powerOfCPUDown + powerOfFECDown + powerOfFD_NLDown + powerOfOFDMDown + powerOfFILETERDown + powerOfDPDDown 
    total_power = total_power_up + total_power_down
    plt.plot(FREQUENCY_MAP, total_power + calculateLeakagePower(total_power), color='black')
    plt.ylabel('Power / W')
    plt.xlabel('Load / MHz')
    plt.savefig('img/totalBaseBandPower.svg', dpi=500)
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    