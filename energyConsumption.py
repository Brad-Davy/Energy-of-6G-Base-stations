import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Class to deal with exceptions
# =============================================================================

class MyException(Exception):
    pass

# =============================================================================
# Define variables
# =============================================================================

LEAKAGE_POWER = 0.1
GOPS_PER_WATT = 40
MY_PARAMETERS = {'BW' : 10, 'Ant' : 12, 'M' : 3/4, 'R' : 2, 'dt' : 100, 'df' : 30}


BASE_BAND_COMPONENTS = {'DPD' : True, 'Filter' : True, 'OFDM' : True, 'FD' : True, 
                      'FD_NL' : True, 'FEC' : True, 'CPU' : True}

RF_COMPONENTS = {} # Need to add these from below

BASE_BAND_SCALING = {'CPU' : [0,0,0,1,0,0],
            'FEC' : [1,1,1,1,1,1],
            'FD_NL' : [1,0,0,2,1,1],
            'FD' : [1,0,0,1,1,1],
            'CRPI' : [1,1,1,1,1,1],
            'DPD' : [1,0,0,1,1,0],
            'FILTER' : [1,0,0,1,1,0],
            'OFDM' : [1,0,0,1,1,0]}

RF_SCALING_TRANSMITTER = {'IQMOD' : [0,1,0,0,1,1],
                          'ATTEN' : [0,1,0,0,1,1],
                          'BUFFER' : [0,1,0,0,1,1],
                          'FOWARD_VOLTAGE_CONTROL' : [0,1,0,0,1,1],
                          'FEEDBACK_VOLTAGE_CONROL' : [0,1,0,0,1,1],
                          'FEEDBACK_MIXER' : [0,1,0,0,1,1],
                          'CLOCK' : [0,1,0,0,1,0],
                          'DAC_CONCVERTER' : [0,1,0,0,1,1],
                          'ADC_CONTROL' : [0,1,0,0,1,1]}

RF_SCALING_RECEIVER = {'LNA1' : [0,1,0,0,1,1],
                       'ATTEN' : [0,1,0,0,1,1],
                       'LNA2' : [0,1,0,0,1,1],
                       'DUAL_MIXER' : [0,1,0,0,1,1],
                       'VGA' : [0,1,0,0,1,1],
                       'CLOCK_GEN' : [0,1,0,0,1,1],
                       'ADC' : [0,1,0,0,1,1]}



# =============================================================================
# Refernce enegry useage for the RF components in mW
# =============================================================================

RF_COMPONENT_POWER_TRANSMITTER = {'IQMOD' : 1000,
                          'ATTEN' : 10,
                          'BUFFER' : 300,
                          'FOWARD_VOLTAGE_CONTROL' : 170,
                          'FEEDBACK_VOLTAGE_CONROL' : 170,
                          'FEEDBACK_MIXER' : 1000,
                          'CLOCK' : 990,
                          'DAC_CONCVERTER' : 1370,
                          'ADC_CONTROL' : 730}


RF_COMPONENT_POWER_RECEIVER = {'LNA1' : 300,
                       'ATTEN' : 10,
                       'LNA2' : 1000,
                       'DUAL_MIXER' : 1000,
                       'VGA' : 650,
                       'CLOCK_GEN' : 990,
                       'ADC' : 1190}



# =============================================================================
# Reference values in download for Macro base station (measured in GOPS)
# which stands for giga operations per second
# =============================================================================

REFERENCE_VALUES_DOWN = {'CPU' : 160,
            'FEC' : 200,
            'FD_NL' : 360,
            'FD' : 60,
            'CRPI' : 30,
            'DPD' : 10,
            'FILTER' : 200,
            'OFDM' : 80}


# =============================================================================
# Reference values for upload
# =============================================================================

REFERENCE_VALUES_UP = {'CPU' : 200,
            'FILTER' : 200,
            'FEC' : 120,
            'FD_NL' : 20,
            'FD' : 60,
            'CRPI' : 80,
            'OFDM' : 80}


# =============================================================================
# Default values for parameters 
# =============================================================================

DEFAULT_VALUE_PARAMETERS = [20, 6, 1, 1, 100, 100]

# =============================================================================
# DEFAULT_BW = 10
# DEFAULT_ANT = 2
# DEFAULT_M = 6
# DEFAULT_R = 5/6
# DEFAULT_DT = 1
# DEFAULT_DR = 1
# =============================================================================

# =============================================================================
# Define functions
# =============================================================================
    
    
def calculateComponentPower(component, current_values):
    
    scaling_for_component = BASE_BAND_SCALING[component]
    powerConsumption = 1

    for idx, components in enumerate(DEFAULT_VALUE_PARAMETERS):
        powerConsumption *= ((current_values[idx] / components) ** scaling_for_component[idx])
    
    return (powerConsumption) 


def returnTotalComponentPower(component, current_values, download = True):
    if download == True:
        return (calculateComponentPower(component, current_values) * REFERENCE_VALUES_DOWN[component]) / GOPS_PER_WATT
    else:
        return (calculateComponentPower(component, current_values) * REFERENCE_VALUES_UP[component]) / GOPS_PER_WATT

def calculateLeakagePower(power):
    
    if isinstance(power, np.ndarray):
        return power * LEAKAGE_POWER
    else:
        raise MyException("Input array needs to be a numpy array.")

    
def returnBaseBandDowlinkEnergy(FREQUENCY_MAP):
    
    powerOfFD = []
    powerOfCPU = []
    powerOfFEC = []
    powerOfFD_NL = []
    powerOfOFDM = []
    powerOfFILETER = []
    powerOfDPD = []
    
    for f in FREQUENCY_MAP:
        
        powerOfFD.append(returnTotalComponentPower(component = 'FD', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfCPU.append(returnTotalComponentPower(component = 'CPU', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfFEC.append(returnTotalComponentPower(component = 'FEC', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfFD_NL.append(returnTotalComponentPower(component = 'FD_NL', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfOFDM.append(returnTotalComponentPower(component = 'OFDM', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfFILETER.append(returnTotalComponentPower(component = 'FILTER', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfDPD.append(returnTotalComponentPower(component = 'DPD', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        
    return np.array(powerOfFD), np.array(powerOfCPU), np.array(powerOfFEC), np.array(powerOfFD_NL), np.array(powerOfOFDM), np.array(powerOfFILETER), np.array(powerOfDPD)
    
def returnBaseBandUplinkEnergy(FREQUENCY_MAP):
    
    powerOfFD = []
    powerOfCPU = []
    powerOfFEC = []
    powerOfFD_NL = []
    powerOfOFDM = []
    powerOfFILETER = []
    
    for f in FREQUENCY_MAP:
        
        powerOfFD.append(returnTotalComponentPower(component = 'FD', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']], download=False))
        powerOfCPU.append(returnTotalComponentPower(component = 'CPU', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']], download=False))
        powerOfFEC.append(returnTotalComponentPower(component = 'FEC', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']], download=False))
        powerOfFD_NL.append(returnTotalComponentPower(component = 'FD_NL', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']], download=False))
        powerOfOFDM.append(returnTotalComponentPower(component = 'OFDM', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']], download=False))
        powerOfFILETER.append(returnTotalComponentPower(component = 'FILTER', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']], download=False))
    
    return np.array(powerOfFD), np.array(powerOfCPU), np.array(powerOfFEC), np.array(powerOfFD_NL), np.array(powerOfOFDM), np.array(powerOfFILETER)
    

def returnFigure2EnergyDownlink(LOAD):
    
    powerOfFD = []
    powerOfCPU = []
    powerOfFEC = []
    powerOfFD_NL = []
    powerOfOFDM = []
    powerOfFILETER = []
    powerOfDPD = []
    
    for l in LOAD:
        
        powerOfFD.append(returnTotalComponentPower(component = 'FD', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l]))
        powerOfCPU.append(returnTotalComponentPower(component = 'CPU', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l]))
        powerOfFEC.append(returnTotalComponentPower(component = 'FEC', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l]))
        powerOfFD_NL.append(returnTotalComponentPower(component = 'FD_NL', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l]))
        powerOfOFDM.append(returnTotalComponentPower(component = 'OFDM', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l]))
        powerOfFILETER.append(returnTotalComponentPower(component = 'FILTER', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l]))
        powerOfDPD.append(returnTotalComponentPower(component = 'DPD', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l]))
        
    return np.array(powerOfFD), np.array(powerOfCPU), np.array(powerOfFEC), np.array(powerOfFD_NL), np.array(powerOfOFDM), np.array(powerOfFILETER), np.array(powerOfDPD)
    
def returnFigure2EnergyUplink(LOAD):
    
    powerOfFD = []
    powerOfCPU = []
    powerOfFEC = []
    powerOfFD_NL = []
    powerOfOFDM = []
    powerOfFILETER = []
    
    for l in LOAD:
        
        powerOfFD.append(returnTotalComponentPower(component = 'FD', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l], download=False))
        powerOfCPU.append(returnTotalComponentPower(component = 'CPU', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l], download=False))
        powerOfFEC.append(returnTotalComponentPower(component = 'FEC', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l], download=False))
        powerOfFD_NL.append(returnTotalComponentPower(component = 'FD_NL', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l], download=False))
        powerOfOFDM.append(returnTotalComponentPower(component = 'OFDM', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l], download=False))
        powerOfFILETER.append(returnTotalComponentPower(component = 'FILTER', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l], download=False))
    
    return np.array(powerOfFD), np.array(powerOfCPU), np.array(powerOfFEC), np.array(powerOfFD_NL), np.array(powerOfOFDM), np.array(powerOfFILETER)
    
    


    
    
    
    
    
    
    
    