import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

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
MY_PARAMETERS = {'BW': 50, 'Ant': 2, 'M': 3/4, 'R': 2, 'dt': 1, 'df': 100}

# =============================================================================
# Parameters descritions:
#     BW = Bandwidth -> Default value: 10.
#     Ant = number of antennas -> Default value: 2.
#     M = Modulation -> Default value: 6.
#     R = Coding rate -> Default value: 5/6.
#     dt = Time-domain duty-cycling -> Default value: 1.
#     df = Frequency-domain duty-cycling -> Default value: 1.
# =============================================================================

# =============================================================================
# Scaling exponents
# =============================================================================

BASE_BAND_SCALING_DOWN = {'CPU': [0, 0, 0, 1, 0, 0],
                          'FEC': [1, 1, 1, 1, 1, 1],
                          'FD_NL': [1, 0, 0, 2, 1, 1],
                          'FD': [1, 0, 0, 1, 1, 1],
                          'CRPI': [1, 1, 1, 1, 1, 1],
                          'DPD': [1, 0, 0, 1, 1, 0],
                          'FILTER': [1, 0, 0, 1, 1, 0],
                          'OFDM': [1, 0, 0, 1, 1, 0]}


BASE_BAND_SCALING_UP = {'CPU': [0, 0, 0, 1, 0, 0],
                        'FEC': [1, 1, 1, 1, 1, 1],
                        'FD_NL': [1, 0, 0, 3, 1, 1],
                        'FD': [1, 0, 0, 1, 1, 1],
                        'CRPI': [1, 1, 1, 1, 1, 1],
                        'DPD': [1, 0, 0, 1, 1, 0],
                        'FILTER': [1, 0, 0, 1, 1, 0],
                        'OFDM': [1, 0, 0, 1, 1, 0]}


RF_SCALING_TRANSMITTER = {'IQMOD': [0, 1, 0, 0, 1, 1],
                          'ATTEN': [0, 1, 0, 0, 1, 1],
                          'BUFFER': [0, 1, 0, 0, 1, 1],
                          'FOWARD_VOLTAGE_CONTROL': [0, 1, 0, 0, 1, 1],
                          'FEEDBACK_VOLTAGE_CONROL': [0, 1, 0, 0, 1, 1],
                          'FEEDBACK_MIXER': [0, 1, 0, 0, 1, 1],
                          'CLOCK': [0, 1, 0, 0, 1, 0],
                          'DAC_CONCVERTER': [0, 1, 0, 0, 1, 1],
                          'ADC_CONTROL': [0, 1, 0, 0, 1, 1]}


RF_SCALING_RECEIVER = {'LNA1': [0, 1, 0, 0, 1, 1],
                       'ATTEN': [0, 1, 0, 0, 1, 1],
                       'LNA2': [0, 1, 0, 0, 1, 1],
                       'DUAL_MIXER': [0, 1, 0, 0, 1, 1],
                       'VGA': [0, 1, 0, 0, 1, 1],
                       'CLOCK_GEN': [0, 1, 0, 0, 1, 1],
                       'ADC': [0, 1, 0, 0, 1, 1]}


# =============================================================================
# Reference values in download for Macro base station (measured in GOPS)
# which stands for giga operations per second
# =============================================================================

REFERENCE_VALUES_DOWN = {'DPD': 160,
                         'FILTER': 200,
                         'CRPI': 360,
                         'OFDM': 80,
                         'FD': 30,
                         'FD_NL': 10,
                         'FEC': 20,
                         'CPU': 200}


# =============================================================================
# Reference values for upload
# =============================================================================

REFERENCE_VALUES_UP = {'CPU': 200,
                       'FILTER': 200,
                       'FEC': 120,
                       'FD_NL': 20,
                       'FD': 60,
                       'CRPI': 360,
                       'OFDM': 80}

# =============================================================================
# Refernce enegry useage for the RF components in mW
# =============================================================================

RF_COMPONENT_POWER_TRANSMITTER = {'IQMOD': 1000,
                                  'ATTEN': 10,
                                  'BUFFER': 300,
                                  'FOWARD_VOLTAGE_CONTROL': 170,
                                  'FEEDBACK_VOLTAGE_CONROL': 170,
                                  'FEEDBACK_MIXER': 1000,
                                  'CLOCK': 990,
                                  'DAC_CONCVERTER': 1370,
                                  'ADC_CONTROL': 730}


RF_COMPONENT_POWER_RECEIVER = {'LNA1': 300,
                               'ATTEN': 10,
                               'LNA2': 1000,
                               'DUAL_MIXER': 1000,
                               'VGA': 650,
                               'CLOCK_GEN': 990,
                               'ADC': 1190}

# =============================================================================
# Default values for parameters
# =============================================================================

DEFAULT_PARAMETER_VALUES = [20, 1, 6, 1, 1, 1]

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

def calculateBBComponentPower(component, current_values, dowload=True):
    """


    Parameters
    ----------
    component : TYPE
        DESCRIPTION.
    current_values : LIST
        [BW, ANT, M, R, DT, DR]
    Returns
    -------
    powerConsumption : TYPE
        DESCRIPTION.

    """
    if dowload == True:
        scaling_for_component = BASE_BAND_SCALING_DOWN[component]
    else:
        scaling_for_component = BASE_BAND_SCALING_UP[component]

    powerConsumption = 1
    for idx, components in enumerate(DEFAULT_PARAMETER_VALUES):
        powerConsumption *= ((current_values[idx] /
                             components) ** scaling_for_component[idx])

    return (powerConsumption)


def returnTotalBBComponentPower(component, current_values, download=True):
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

def calculateRFComponentPower(component, current_values, transmitter=True):
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
        powerConsumption *= ((current_values[idx] /
                             default_values) ** scaling_for_component[idx])

    return powerConsumption


def returnTotalRFComponentPower(component, current_values, transmitter=True):
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


def baseBandUploadPower(parameters=MY_PARAMETERS):

    # =============================================================================
    # Upload
    # =============================================================================
    # BW, M,, R, Ant, dt, df
    FDPower = returnTotalBBComponentPower(component='FD', current_values=[
                                          parameters['BW'], parameters['M'], parameters['R'], parameters['Ant'], parameters['dt'], parameters['df']], download=False)
    CPUPower = returnTotalBBComponentPower(component='CPU', current_values=[
        parameters['BW'], parameters['M'], parameters['R'], parameters['Ant'], parameters['dt'], parameters['df']], download=False)
    FECPower = returnTotalBBComponentPower(component='FEC', current_values=[
        parameters['BW'], parameters['M'], parameters['R'], parameters['Ant'], parameters['dt'], parameters['df']], download=False)
    FD_NLPower = returnTotalBBComponentPower(component='FD_NL', current_values=[
        parameters['BW'], parameters['M'], parameters['R'], parameters['Ant'], parameters['dt'], parameters['df']], download=False)
    OFDMPower = returnTotalBBComponentPower(component='OFDM', current_values=[
        parameters['BW'], parameters['M'], parameters['R'], parameters['Ant'], parameters['dt'], parameters['df']], download=False)
    FILTERPower = returnTotalBBComponentPower(component='FILTER', current_values=[
        parameters['BW'], parameters['M'], parameters['R'], parameters['Ant'], parameters['dt'], parameters['df']], download=False)

    return FDPower + CPUPower + FECPower + FD_NLPower + OFDMPower + FILTERPower


def baseBandDownloadPower(parameters=MY_PARAMETERS):

    # =============================================================================
    # Download
    # =============================================================================

    FDPower = returnTotalBBComponentPower(component='FD', current_values=[
                                          parameters['BW'], parameters['M'], parameters['R'], parameters['Ant'], parameters['dt'], parameters['df']])
    CPUPower = returnTotalBBComponentPower(component='CPU', current_values=[
        parameters['BW'], parameters['M'], parameters['R'], parameters['Ant'], parameters['dt'], parameters['df']])
    FECPower = returnTotalBBComponentPower(component='FEC', current_values=[
        parameters['BW'], parameters['M'], parameters['R'], parameters['Ant'], parameters['dt'], parameters['df']])
    FD_NLPower = returnTotalBBComponentPower(component='FD_NL', current_values=[
        parameters['BW'], parameters['M'], parameters['R'], parameters['Ant'], parameters['dt'], parameters['df']])
    OFDMPower = returnTotalBBComponentPower(component='OFDM', current_values=[
        parameters['BW'], parameters['M'], parameters['R'], parameters['Ant'], parameters['dt'], parameters['df']])
    FILTERPower = returnTotalBBComponentPower(component='FILTER', current_values=[
        parameters['BW'], parameters['M'], parameters['R'], parameters['Ant'], parameters['dt'], parameters['df']])
    DPDPower = returnTotalBBComponentPower(component='DPD', current_values=[
        parameters['BW'], parameters['M'], parameters['R'], parameters['Ant'], parameters['dt'], parameters['df']])

    return FDPower + CPUPower + FECPower + FD_NLPower + OFDMPower + FILTERPower + DPDPower


def RFTransmitterPower(parameters=MY_PARAMETERS):

    IQPower = returnTotalRFComponentPower(component='IQMOD', current_values=[
                                          parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    ATTENPower = returnTotalRFComponentPower(component='ATTEN', current_values=[
                                             parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    BUFFPOwer = returnTotalRFComponentPower(component='BUFFER', current_values=[
                                            parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    FVCPower = returnTotalRFComponentPower(component='FOWARD_VOLTAGE_CONTROL', current_values=[
                                           parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    FECVPower = returnTotalRFComponentPower(component='FEEDBACK_VOLTAGE_CONROL', current_values=[
                                            parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    FMPower = returnTotalRFComponentPower(component='FEEDBACK_MIXER', current_values=[
                                          parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    CLKPower = returnTotalRFComponentPower(component='CLOCK', current_values=[
                                           parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    DCPower = returnTotalRFComponentPower(component='DAC_CONCVERTER', current_values=[
                                          parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])
    ADCPower = returnTotalRFComponentPower(component='ADC_CONTROL', current_values=[
                                           parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']])

    return IQPower + ATTENPower + BUFFPOwer + FVCPower + FECVPower + FMPower + CLKPower + DCPower + ADCPower


def RFReceiverPower(parameters=MY_PARAMETERS):

    powerOfLNA1 = returnTotalRFComponentPower(component='LNA1', current_values=[
                                              parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], transmitter=False)
    powerATTEN = returnTotalRFComponentPower(component='ATTEN', current_values=[
                                             parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], transmitter=False)
    powerOfLNA2 = returnTotalRFComponentPower(component='LNA2', current_values=[
                                              parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], transmitter=False)
    powerOfDUAL_MIXER = returnTotalRFComponentPower(component='DUAL_MIXER', current_values=[
                                                    parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], transmitter=False)
    powerOfOVGA = returnTotalRFComponentPower(component='VGA', current_values=[
                                              parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], transmitter=False)
    powerOfCLKGEN = returnTotalRFComponentPower(component='CLOCK_GEN', current_values=[
                                                parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], transmitter=False)
    powerOfADC = returnTotalRFComponentPower(component='ADC', current_values=[
                                             parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']], transmitter=False)

    return powerOfLNA1 + powerATTEN + powerOfLNA2 + powerOfDUAL_MIXER + powerOfOVGA + powerOfCLKGEN + powerOfADC


def returnPAPower(parameters=MY_PARAMETERS):
    load = parameters['df']
    total_power_PA = [float(i) for i in open(
        'powerAmplifierLoad.txt', 'r').read().split('\n')]
    LOAD = np.linspace(0, 0.99, 100)
    interpolated_data = interp1d(LOAD, total_power_PA)
    return 0.97*interpolated_data(load)


def returnOverHead(BBPower, RFPower, PAPower):
    coolingOH = 0.1
    DC_DCOH = 0.05
    AC_DCOH = 0.1
    factor = (((1 + coolingOH) * (1 + DC_DCOH) * (1 + AC_DCOH)) - 1)
    return (BBPower + RFPower + PAPower) * factor


def returnTotalPower(parameters=MY_PARAMETERS):
    """

    Parameters
    ----------
    parameters : TYPE, optional
        DESCRIPTION. The default is MY_PARAMETERS.

    Returns
    -------
    None.

    """
    baseBandPower = baseBandUploadPower(
        parameters=parameters) + baseBandDownloadPower(parameters=parameters)

    RFPower = (RFTransmitterPower(parameters=parameters) +
               RFReceiverPower(parameters=parameters)) / 1000
    PAPower = returnPAPower(parameters=parameters)
    OHPower = returnOverHead(baseBandPower*2, RFPower*2, PAPower)

    return baseBandPower*2, RFPower*2, PAPower, OHPower


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
