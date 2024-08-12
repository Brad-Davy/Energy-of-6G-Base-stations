from flask import Flask, request, jsonify
from energyConsumption import *

app = Flask(__name__)


@app.route("/power-component-consumption/<bw>/<ant>/<M>/<R>/<dt>/<df>")
def returnComponentPowerConsumption(bw, ant, M, R, dt, df):
    parameters = {'BW' : float(bw), 'Ant' : int(ant), 'M' : float(M), 'R' : float(R), 'dt' : int(dt), 'df' : int(df)}
    BB, RF, PA, Oh = returnTotalPower(parameters)

    return jsonify({'BB' : BB, 'RF' : RF, 'PA' : PA, 'Oh' : Oh}), 200


@app.route("/power-consumption/<bw>/<ant>/<M>/<R>/<dt>/<df>")
def returnPowerConsumption(bw, ant, M, R, dt, df):
    parameters = {'BW' : float(bw), 'Ant' : int(ant), 'M' : float(M), 'R' : float(R), 'dt' : int(dt), 'df' : int(df)}
    power =  sum(returnTotalPower(parameters))
    print(power)
    parameters['power'] = power
    return jsonify(parameters), 200


if __name__ == '__main__':

    app.run(debug=True, host="0.0.0.0", port=8000)