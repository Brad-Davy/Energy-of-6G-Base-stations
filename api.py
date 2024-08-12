import requests

def getPowerConsumption(parameters):
    x = requests.get('http://0.0.0.0:8000/power-consumption/{}/{}/{}/{}/{}/{}'.format(parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']))
    return x.json()

def getComponentPowerConsumption(parameters):
    x = requests.get('http://0.0.0.0:8000/power-component-consumption/{}/{}/{}/{}/{}/{}'.format(parameters['BW'], parameters['Ant'], parameters['M'], parameters['R'], parameters['dt'], parameters['df']))
    return x.json()