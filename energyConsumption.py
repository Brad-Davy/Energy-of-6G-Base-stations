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
MY_PARAMETERS = {'BW' : 50, 'Ant' : 2, 'M' : 3/4, 'R' : 2, 'dt' : 1, 'df' : 100}

# =============================================================================
# Parameters descritions:
#     BW = Bandwidth -> Default value: 10.
#     Ant = number of antennas -> Default value: 2.
#     M = Modulation -> Default value: 6.
#     R = Coding rate -> Default value: 5/6.
#     dt = Time-domain duty-cycling -> Default value: 1.
#     df = Frequency-domain duty-cycling -> Default value: 1.
# =============================================================================
    

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


def baseBandUploadPower(parameters = MY_PARAMETERS):
    
    # =============================================================================
    # Upload    
    # =============================================================================
    
    FDPower = returnTotalBBComponentPower(component = 'FD', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], download=False)
    CPUPower =  returnTotalBBComponentPower(component = 'CPU', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], download=False)
    FECPower =  returnTotalBBComponentPower(component = 'FEC', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], download=False)
    FD_NLPower =  returnTotalBBComponentPower(component = 'FD_NL', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], download=False)
    OFDMPower =  returnTotalBBComponentPower(component = 'OFDM', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], download=False)
    FILTERPower =  returnTotalBBComponentPower(component = 'FILTER', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], download=False)
    
    return FDPower + CPUPower + FECPower + FD_NLPower + OFDMPower + FILTERPower

def baseBandDownloadPower(parameters = MY_PARAMETERS):
    
    # =============================================================================
    # Download   
    # =============================================================================
    
    FDPower = returnTotalBBComponentPower(component = 'FD', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    CPUPower =  returnTotalBBComponentPower(component = 'CPU', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    FECPower =  returnTotalBBComponentPower(component = 'FEC', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    FD_NLPower =  returnTotalBBComponentPower(component = 'FD_NL', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    OFDMPower =  returnTotalBBComponentPower(component = 'OFDM', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    FILTERPower =  returnTotalBBComponentPower(component = 'FILTER', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    DPDPower =  returnTotalBBComponentPower(component = 'DPD', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    
    return FDPower + CPUPower + FECPower + FD_NLPower + OFDMPower + FILTERPower + DPDPower

def RFTransmitterPower(parameters = MY_PARAMETERS):
    
    
    IQPower = returnTotalRFComponentPower(component = 'IQMOD', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    ATTENPower = returnTotalRFComponentPower(component = 'ATTEN', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    BUFFPOwer = returnTotalRFComponentPower(component = 'BUFFER', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    FVCPower = returnTotalRFComponentPower(component = 'FOWARD_VOLTAGE_CONTROL', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    FECVPower = returnTotalRFComponentPower(component = 'FEEDBACK_VOLTAGE_CONROL', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    FMPower = returnTotalRFComponentPower(component = 'FEEDBACK_MIXER', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    CLKPower = returnTotalRFComponentPower(component = 'CLOCK', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    DCPower = returnTotalRFComponentPower(component = 'DAC_CONCVERTER', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    ADCPower = returnTotalRFComponentPower(component = 'ADC_CONTROL', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    
    return IQPower + ATTENPower + BUFFPOwer + FVCPower + FECVPower + FMPower + CLKPower + DCPower + ADCPower

def RFReceiverPower(parameters = MY_PARAMETERS):
    
    print(parameters)
    powerOfLNA1 = returnTotalRFComponentPower(component = 'LNA1', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], transmitter = False)
    powerATTEN = returnTotalRFComponentPower(component = 'ATTEN', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], transmitter = False)
    powerOfLNA2 = returnTotalRFComponentPower(component = 'LNA2', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], transmitter = False)
    powerOfDUAL_MIXER = returnTotalRFComponentPower(component = 'DUAL_MIXER', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], transmitter = False)
    powerOfOVGA = returnTotalRFComponentPower(component = 'VGA', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], transmitter = False)
    powerOfCLKGEN =  returnTotalRFComponentPower(component = 'CLOCK_GEN', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], transmitter = False)
    powerOfADC = returnTotalRFComponentPower(component = 'ADC', current_values=[parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], transmitter = False)
    
    return powerOfLNA1 + powerATTEN + powerOfLNA2 + powerOfDUAL_MIXER + powerOfOVGA + powerOfCLKGEN + powerOfADC

def returnPAPower(parameters = MY_PARAMETERS):
    load = parameters['dt']
    total_power_PA = [float(i) for i in open('powerAmplifierLoad.txt', 'r').read().split('\n')]
    return total_power_PA[load]

def returnOverHead(BBPower, RFPower, PAPower):
    coolingOH = 0.05
    DC_DCOH = 0.05
    AC_DCOH = 0.1
    factor =  (((1 + coolingOH) * (1 + DC_DCOH) * (1 + AC_DCOH)) - 1)
    print(factor)
    print(BBPower, RFPower, PAPower)
    return (BBPower + RFPower + PAPower) * factor
    

def returnTotalPower(parameters = MY_PARAMETERS):
    """

    Parameters
    ----------
    parameters : TYPE, optional
        DESCRIPTION. The default is MY_PARAMETERS.

    Returns
    -------
    None.

    """

    baseBandPower = baseBandUploadPower(parameters = parameters) + baseBandDownloadPower(parameters = parameters)
    RFPower = (RFTransmitterPower(parameters = parameters) + RFReceiverPower(parameters = parameters)) / 1000
    PAPower = returnPAPower(parameters = parameters)
    OHPower = returnOverHead(baseBandPower, RFPower, PAPower)
    
    return baseBandPower, RFPower, PAPower, OHPower
    