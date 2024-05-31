import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Define variables
# =============================================================================

GOPS_PER_WATT = 40

scalings = {'CPU' : [0,0,0,1,0,0],
            'FEC' : [1,1,1,1,1,1],
            'FD_NL' : [1,0,0,2,1,1],
            'FD' : [1,0,0,1,1,1],
            'CRPI' : [1,1,1,1,1,1],
            'DPD' : [1,0,0,1,1,0]}

# =============================================================================
# Reference values in download for Macro base station (measured in GOPS)
# which stands for giga operations per second
# =============================================================================

REFERENCE_VALUES_DOWN = {'CPU' : 160,
            'FEC' : 200,
            'FD_NL' : 360,
            'FD' : 60,
            'CRPI' : 30,
            'DPD' : 10}


# =============================================================================
# Reference values for upload
# =============================================================================

REFERENCE_VALUES_UP = {'CPU' : 200,
            'FEC' : 200,
            'FD_NL' : 360,
            'FD' : 80,
            'CRPI' : 30,
            'DPD' : 10}


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
    
    scaling_for_component = scalings[component]
    powerConsumption = 1

    for idx, components in enumerate(DEFAULT_VALUE_PARAMETERS):
        powerConsumption *= ((current_values[idx] / components) ** scaling_for_component[idx])
    
    return (powerConsumption) 


def returnTotalComponentPower(component, current_values):
    print(calculateComponentPower(component, current_values))
    return (calculateComponentPower(component, current_values) * REFERENCE_VALUES_DOWN[component]) / GOPS_PER_WATT


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    