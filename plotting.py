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
%matplotlib 

plt.rcParams['font.family'] = 'Serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.linewidth'] = 1
plt.rcParams["figure.autolayout"] = True
cm = 1/2.54  # centimeters in inches

FREQUENCY_MAP = np.linspace(0, 100, 100)
LOAD = np.linspace(0,100,100)

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
    
    # =============================================================================
    # Paper data    
    # =============================================================================
    load_frequency = np.array([0.0, 0.49, 0.90, 1.55, 2.36, 5.46, 9.54, 14.59, 21.60, 31.54, 36.92, 45.40, 56.97, 69.19, 79.79, 85.66, 93.48, 100.70])
    power_frequency = [398.8, 457.02, 490.23, 519.26, 531.66, 560.49, 601.70, 659.45, 729.51, 820.09, 865.35, 926.98, 1009.12, 1095.36, 1165.1, 1202.02, 1263.70, 1300.6]
    
    interpolated_data = interp1d(load_frequency, power_frequency)
    power_frequency_interpolated = [interpolated_data(i) for i in LOAD]
    
    load_time = []
    power_time = []
    
    fig = plt.figure(figsize = (15*cm, 15*cm))
    
    # =============================================================================
    # Baseband power consumption
    # =============================================================================
    
    powerOfFDUp, powerOfCPUUp, powerOfFECUp, powerOfFD_NLUp, powerOfOFDMUp, powerOfFILETERUp = returnFigure2EnergyUplink(LOAD)
    powerOfFDDown, powerOfCPUDown, powerOfFECDown, powerOfFD_NLDown, powerOfOFDMDown, powerOfFILETERDown, powerOfDPDDown = returnFigure2EnergyDownlink(LOAD)
   
    total_power_BB_up = powerOfFDUp + powerOfCPUUp + powerOfFECUp + powerOfFD_NLUp + powerOfOFDMUp + powerOfFILETERUp 
    total_power_BB_down = powerOfFDDown + powerOfCPUDown + powerOfFECDown + powerOfFD_NLDown + powerOfOFDMDown + powerOfFILETERDown + powerOfDPDDown 
    total_power_BB = np.array((total_power_BB_up + total_power_BB_down) + calculateLeakagePower(total_power_BB_up + total_power_BB_down))
    
    # =============================================================================
    # RF power consumption
    # =============================================================================
    
    powerOfIQ_TRANSMITTER, powerOfATTEN_TRANSMITTER, powerOfBUFF_TRANSMITTER, powerOfFVC_TRANSMITTER, powerOfOFEVC_TRANSMITTER, powerOfFM_TRANSMITTER, powerOfCLK_TRANSMITTER, powerOfDC_TRANSMITTER, powerOfADC_TRANSMITTER = returnFigure2RFTransmitterEnergy(LOAD) 
    powerOfLNA1_RECEIVER, powerOfATTEN_RECEIVER, powerOfLNA2_RECEIVER, powerOfDUAL_MIXER_RECEIVER, powerOfOVGA_RECEIVER, powerOfCLKGEN_RECEIVER, powerOfADC_RECEIVER = returnFigure2RFReceiverEnergy(LOAD)  
    RF_TRANSMITTER_TOTAL = np.array(powerOfIQ_TRANSMITTER + powerOfATTEN_TRANSMITTER + powerOfBUFF_TRANSMITTER + powerOfFVC_TRANSMITTER + powerOfOFEVC_TRANSMITTER + powerOfFM_TRANSMITTER + powerOfCLK_TRANSMITTER + powerOfDC_TRANSMITTER + powerOfADC_TRANSMITTER) / 1000
    RF_RECEIVER_TOTAL = np.array(powerOfLNA1_RECEIVER + powerOfATTEN_RECEIVER + powerOfLNA2_RECEIVER + powerOfDUAL_MIXER_RECEIVER + powerOfOVGA_RECEIVER + powerOfCLKGEN_RECEIVER + powerOfADC_RECEIVER) / 1000
    total_power_RF = RF_TRANSMITTER_TOTAL + RF_RECEIVER_TOTAL
    
    
    # =============================================================================
    # Power amplifier power consumption    
    # =============================================================================
    
    total_power_PA = [float(i) for i in open('powerAmplifier.txt', 'r').read().split('\n')]
    
    # =============================================================================
    # Overhead power coonsumption
    # =============================================================================

    total_power_Oh = returnOverHead(total_power_BB, total_power_RF, total_power_PA)

    total_power = total_power_BB + total_power_PA + total_power_RF + total_power_Oh
    
    plt.plot(LOAD, total_power_PA, color = CB91_Green, label = 'Power amplifier')
    plt.plot(LOAD, total_power_BB, color = CB91_Blue, label = 'Baseband')
    plt.plot(LOAD, total_power_RF, color = CB91_Amber, label = 'Radio')
    
    plt.plot(LOAD, total_power_Oh, color = CB91_Violet, label = 'Overhead')
    plt.plot(load_frequency, power_frequency, color = 'red', label = '(Desset et al)')
    plt.plot(LOAD, total_power + calculateLeakagePower(total_power), color='black', linestyle = 'dotted', label = 'total')
   
    plt.ylabel('Power / W')
    plt.xlabel('Load / %')
    plt.legend()
    plt.savefig('img/totalBaseBandPower.svg', dpi=500)
    

totalPowerBaseBand()   
#reproduceFigure2()
    

    
    
    
    
    
    
    
    
    
    