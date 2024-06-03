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
MY_PARAMETERS = {'BW' : 20, 'Ant' : 4, 'M' : 3/4, 'R' : 2, 'dt' : 100, 'df' : 30}


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

DEFAULT_PARAMETER_VALUES = [20, 6, 1, 1, 100, 100]

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


# =============================================================================
# Logic for calculating the power from the baseband units
# =============================================================================
    
def calculateBBComponentPower(component, current_values):
    """
    

    Parameters
    ----------
    component : TYPE
        DESCRIPTION.
    current_values : TYPE
        DESCRIPTION.

    Returns
    -------
    powerConsumption : TYPE
        DESCRIPTION.

    """
    
    scaling_for_component = BASE_BAND_SCALING[component]
    powerConsumption = 1

    for idx, components in enumerate(DEFAULT_PARAMETER_VALUES):
        powerConsumption *= ((current_values[idx] / components) ** scaling_for_component[idx])
    
    return (powerConsumption) 


def returnTotalBBComponentPower(component, current_values, download = True):
    """
    

    Parameters
    ----------
    component : TYPE
        DESCRIPTION.
    current_values : TYPE
        DESCRIPTION.
    download : TYPE, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    if download == True:
        return (calculateBBComponentPower(component, current_values) * REFERENCE_VALUES_DOWN[component]) / GOPS_PER_WATT
    else:
        return (calculateBBComponentPower(component, current_values) * REFERENCE_VALUES_UP[component]) / GOPS_PER_WATT

def calculateLeakagePower(power):
    """
    

    Parameters
    ----------
    power : TYPE
        DESCRIPTION.

    Raises
    ------
    MyException
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    if isinstance(power, np.ndarray):
        return power * LEAKAGE_POWER
    else:
        raise MyException("Input array needs to be a numpy array.")

    
def returnBaseBandDowlinkEnergy(FREQUENCY_MAP):
    """
    

    Parameters
    ----------
    FREQUENCY_MAP : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    powerOfFD = []
    powerOfCPU = []
    powerOfFEC = []
    powerOfFD_NL = []
    powerOfOFDM = []
    powerOfFILETER = []
    powerOfDPD = []
    
    for f in FREQUENCY_MAP:
        
        powerOfFD.append(returnTotalBBComponentPower(component = 'FD', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfCPU.append(returnTotalBBComponentPower(component = 'CPU', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfFEC.append(returnTotalBBComponentPower(component = 'FEC', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfFD_NL.append(returnTotalBBComponentPower(component = 'FD_NL', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfOFDM.append(returnTotalBBComponentPower(component = 'OFDM', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfFILETER.append(returnTotalBBComponentPower(component = 'FILTER', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfDPD.append(returnTotalBBComponentPower(component = 'DPD', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        
    return np.array(powerOfFD), np.array(powerOfCPU), np.array(powerOfFEC), np.array(powerOfFD_NL), np.array(powerOfOFDM), np.array(powerOfFILETER), np.array(powerOfDPD)
    
def returnBaseBandUplinkEnergy(FREQUENCY_MAP):
    """
    

    Parameters
    ----------
    FREQUENCY_MAP : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    powerOfFD = []
    powerOfCPU = []
    powerOfFEC = []
    powerOfFD_NL = []
    powerOfOFDM = []
    powerOfFILETER = []
    
    for f in FREQUENCY_MAP:
        
        powerOfFD.append(returnTotalBBComponentPower(component = 'FD', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']], download=False))
        powerOfCPU.append(returnTotalBBComponentPower(component = 'CPU', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']], download=False))
        powerOfFEC.append(returnTotalBBComponentPower(component = 'FEC', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']], download=False))
        powerOfFD_NL.append(returnTotalBBComponentPower(component = 'FD_NL', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']], download=False))
        powerOfOFDM.append(returnTotalBBComponentPower(component = 'OFDM', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']], download=False))
        powerOfFILETER.append(returnTotalBBComponentPower(component = 'FILTER', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']], download=False))
    
    return np.array(powerOfFD), np.array(powerOfCPU), np.array(powerOfFEC), np.array(powerOfFD_NL), np.array(powerOfOFDM), np.array(powerOfFILETER)
    

# =============================================================================
# Logic to determine the power used in the RF components 
# =============================================================================

def calculateRFComponentPower(component, current_values, transmitter = True):
    """
    

    Parameters
    ----------
    component : TYPE
        DESCRIPTION.
    current_values : TYPE
        DESCRIPTION.

    Returns
    -------
    powerConsumption : TYPE
        DESCRIPTION.

    """
    
    if transmitter == True:
        scaling_for_component = RF_SCALING_TRANSMITTER[component]
        
    else:
        scaling_for_component = RF_SCALING_RECEIVER[component]
        
    powerConsumption = 1

    for idx, default_values in enumerate(DEFAULT_PARAMETER_VALUES):
        powerConsumption *= ((current_values[idx] / default_values) ** scaling_for_component[idx])
    
    return powerConsumption

def returnTotalRFComponentPower(component, current_values, transmitter = True):
    """
    

    Parameters
    ----------
    component : TYPE
        DESCRIPTION.
    current_values : TYPE
        DESCRIPTION.
    download : TYPE, optional
        DESCRIPTION. The default is True.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    if transmitter == True:
        return (calculateRFComponentPower(component, current_values) * RF_COMPONENT_POWER_TRANSMITTER[component]) 
    else:
        return (calculateRFComponentPower(component, current_values, transmitter=False) * RF_COMPONENT_POWER_RECEIVER[component]) 

def returnRFTransmitterEnergy(FREQUENCY_MAP):
    """
    

    Parameters
    ----------
    FREQUENCY_MAP : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    powerOfIQ = []
    powerOfATTEN = []
    powerOfBUFF = []
    powerOfFVC = []
    powerOfOFEVC = []
    powerOfFM = []
    powerOfCLK = []
    powerOfDC = []
    powerOfADC = []
    
    for f in FREQUENCY_MAP:
        
        powerOfIQ.append(returnTotalRFComponentPower(component = 'IQMOD', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfATTEN.append(returnTotalRFComponentPower(component = 'ATTEN', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfBUFF.append(returnTotalRFComponentPower(component = 'BUFFER', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfFVC.append(returnTotalRFComponentPower(component = 'FOWARD_VOLTAGE_CONTROL', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfOFEVC.append(returnTotalRFComponentPower(component = 'FEEDBACK_VOLTAGE_CONROL', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfFM.append(returnTotalRFComponentPower(component = 'FEEDBACK_MIXER', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfCLK.append(returnTotalRFComponentPower(component = 'CLOCK', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfDC.append(returnTotalRFComponentPower(component = 'DAC_CONCVERTER', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
        powerOfADC.append(returnTotalRFComponentPower(component = 'ADC_CONTROL', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']]))
               
        
    return np.array(powerOfIQ), np.array(powerOfATTEN), np.array(powerOfBUFF), np.array(powerOfFVC), np.array(powerOfOFEVC), np.array(powerOfFM), np.array(powerOfCLK), np.array(powerOfDC), np.array(powerOfADC)
    

def returnRFReceiverEnergy(FREQUENCY_MAP):
    """
    

    Parameters
    ----------
    FREQUENCY_MAP : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """

    powerOfLNA1 = []
    powerOfATTEN = []
    powerOfLNA2 = []
    powerOfDUAL_MIXER = []
    powerOfOVGA = []
    powerOfCLKGEN = []
    powerOfADC = []
    
    for f in FREQUENCY_MAP:
        
        powerOfLNA1.append(returnTotalRFComponentPower(component = 'LNA1', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']], transmitter = False))
        powerOfATTEN.append(returnTotalRFComponentPower(component = 'ATTEN', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']], transmitter = False))
        powerOfLNA2.append(returnTotalRFComponentPower(component = 'LNA2', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']], transmitter = False))
        powerOfDUAL_MIXER.append(returnTotalRFComponentPower(component = 'DUAL_MIXER', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']], transmitter = False))
        powerOfOVGA.append(returnTotalRFComponentPower(component = 'VGA', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']], transmitter = False))
        powerOfCLKGEN.append(returnTotalRFComponentPower(component = 'CLOCK_GEN', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']], transmitter = False))
        powerOfADC.append(returnTotalRFComponentPower(component = 'ADC', current_values=[f, MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], MY_PARAMETERS['df']], transmitter = False))
               
    return np.array(powerOfLNA1), np.array(powerOfATTEN), np.array(powerOfLNA2), np.array(powerOfDUAL_MIXER), np.array(powerOfOVGA), np.array(powerOfCLKGEN), np.array(powerOfADC)

# =============================================================================
# Some code to reproduce the figure 2 from the Desset et al paper
# =============================================================================

def returnFigure2EnergyDownlink(LOAD):
    """
    

    Parameters
    ----------
    LOAD : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    powerOfFD = []
    powerOfCPU = []
    powerOfFEC = []
    powerOfFD_NL = []
    powerOfOFDM = []
    powerOfFILETER = []
    powerOfDPD = []
    
    for l in LOAD:
        
        powerOfFD.append(returnTotalBBComponentPower(component = 'FD', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l]))
        powerOfCPU.append(returnTotalBBComponentPower(component = 'CPU', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l]))
        powerOfFEC.append(returnTotalBBComponentPower(component = 'FEC', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l]))
        powerOfFD_NL.append(returnTotalBBComponentPower(component = 'FD_NL', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l]))
        powerOfOFDM.append(returnTotalBBComponentPower(component = 'OFDM', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l]))
        powerOfFILETER.append(returnTotalBBComponentPower(component = 'FILTER', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l]))
        powerOfDPD.append(returnTotalBBComponentPower(component = 'DPD', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l]))
        
    return np.array(powerOfFD), np.array(powerOfCPU), np.array(powerOfFEC), np.array(powerOfFD_NL), np.array(powerOfOFDM), np.array(powerOfFILETER), np.array(powerOfDPD)
    
def returnFigure2EnergyUplink(LOAD):
    """
    

    Parameters
    ----------
    LOAD : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    powerOfFD = []
    powerOfCPU = []
    powerOfFEC = []
    powerOfFD_NL = []
    powerOfOFDM = []
    powerOfFILETER = []
    
    for l in LOAD:
        
        powerOfFD.append(returnTotalBBComponentPower(component = 'FD', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l], download=False))
        powerOfCPU.append(returnTotalBBComponentPower(component = 'CPU', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l], download=False))
        powerOfFEC.append(returnTotalBBComponentPower(component = 'FEC', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l], download=False))
        powerOfFD_NL.append(returnTotalBBComponentPower(component = 'FD_NL', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l], download=False))
        powerOfOFDM.append(returnTotalBBComponentPower(component = 'OFDM', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l], download=False))
        powerOfFILETER.append(returnTotalBBComponentPower(component = 'FILTER', current_values=[MY_PARAMETERS['BW'], MY_PARAMETERS['Ant'], MY_PARAMETERS['M'], MY_PARAMETERS['R'], MY_PARAMETERS['dt'], l], download=False))
    
    return np.array(powerOfFD), np.array(powerOfCPU), np.array(powerOfFEC), np.array(powerOfFD_NL), np.array(powerOfOFDM), np.array(powerOfFILETER)
    




    
    
    
    
    
    
    
    