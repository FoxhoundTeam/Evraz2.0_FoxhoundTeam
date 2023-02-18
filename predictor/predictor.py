from scipy.optimize import curve_fit
import numpy as np
from datetime import datetime, timedelta

TEMP = [
    'SM_Exgauster\\[2:{}]'.format(27+i) for i in range(0, 9)
]

VIBR_HOR = [
    'SM_Exgauster\\[2:0]', 'SM_Exgauster\\[2:3]',
    'SM_Exgauster\\[2:6]', 'SM_Exgauster\\[2:9]'
]

VIBR_VERT = [
    'SM_Exgauster\\[2:0]', 'SM_Exgauster\\[2:3]',
    'SM_Exgauster\\[2:6]', 'SM_Exgauster\\[2:9]'
]

VIBR_AXIS = [
    'SM_Exgauster\\[2:0]', 'SM_Exgauster\\[2:3]',
    'SM_Exgauster\\[2:6]', 'SM_Exgauster\\[2:9]'
]

BEARINGS_WITH_VIBS = [0, 1, 6, 7]

# function for linear trend
def linear(x, a, b):
    return a * x + b

class Predictor:
    def __init__(self):

        # data structure
        # 9 different bearings (with provided amplitude)
        # each bearing parameter is sotred as dict

        # timestamps (stored in seconds relative to 2000.01.01)
        self.t = []
        
        # storage for values of temperature and vibrations
        self.data_value = [{} for i in range(9)]

        # storage for alarm values of temperature and vibrations 
        self.data_alarm = [{'Temperature' : 8000.0} for i in range(9)]

        # storage for waning values of temperature and vibrations 
        self.data_warn = [{'Temperature' : 8000.0} for i in range(9)]

        for i in BEARINGS_WITH_VIBS:
            for key in ['Vibration_horizntal', 'Vibration_vertical', 'Vibration_axis']:
                self.data_warn[i][key] = 1
                self.data_alarm[i][key] = 1

        self.linear_coef = [{} for i in range(9)]
        self.linear_coef_std = [{} for i in range(9)]

        for i in BEARINGS_WITH_VIBS:
            for key in ['Vibration_horizntal', 'Vibration_vertical', 'Vibration_axis']:
                self.linear_coef[i][key] = np.array([0, 0])
                self.linear_coef_std[i][key] = np.array([0, 0])



    def set_alarm_val(self, key, ind, value):
        self.data_alarm[ind][key] = value

    def set_warn_val(self, key, ind, value):
        self.data_alarm[ind][key] = value

    def write_mes(self, mes):

        date = mes['moment'].replace('T', ' ')[2:-7]
        date = (datetime.strptime(date, '%y-%m-%d %H:%M:%S') \
            -datetime(2022,1,1)).total_seconds() / (3600 * 24)


        # check if this particulat timestamp is not already in data
        if True: #date not in self.t :
            self.t.append(date)

            # hard code mapping from xlsx-file

            # add temperature
            for key, i in zip(iter(TEMP), range(9)):

                value = mes[key]
                if type(value) != float:
                    value = self.data_value[i]['Temperature'][-1]

                if 'Temperature' in self.data_value[i].keys():
                    self.data_value[i]['Temperature'].append(value)
                else:
                    self.data_value[i]['Temperature'] = [value]


            # add horizontal vibrations
            for key, i in zip(iter(VIBR_HOR), [0, 1, 6, 7]):

                value = mes[key]
                if type(value) != float:
                    if 'Vibration_horizntal' in self.data_value[i].keys():
                        value = self.data_value[i]['Vibration_horizntal'][-1]
                    else:
                        value = 0.

                if 'Vibration_horizntal' in self.data_value[i].keys():
                    self.data_value[i]['Vibration_horizntal'].append(value)
                else:
                    self.data_value[i]['Vibration_horizntal'] = [value]

            # add vertical vibrations
            for key, i in zip(iter(VIBR_VERT), [0, 1, 6, 7]):

                value = mes[key]
                if type(value) != float:
                    if 'Vibration_vertical' in self.data_value[i].keys():
                        value = self.data_value[i]['Vibration_vertical'][-1]
                    else:
                        value = 0.

                if 'Vibration_vertical' in self.data_value[i].keys():
                    self.data_value[i]['Vibration_vertical'].append(value)
                else:
                    self.data_value[i]['Vibration_vertical'] = [value]

            # add horizontal vibrations
            for key, i in zip(iter(VIBR_AXIS), [0, 1, 6, 7]):

                value = mes[key]
                if type(value) != float:
                    if 'Vibration_axis' in self.data_value[i].keys():
                        value = self.data_value[i]['Vibration_axis'][-1]
                    else:
                        value = 0.

                if 'Vibration_axis' in self.data_value[i].keys():
                    self.data_value[i]['Vibration_axis'].append(value)
                else:
                    self.data_value[i]['Vibration_axis'] = [value]

    def fit(self):
        
        for i in BEARINGS_WITH_VIBS:
            for key in ['Vibration_horizntal', 'Vibration_vertical', 'Vibration_axis']:

                popt, pcov = curve_fit(
                    linear,
                    self.t,
                    self.data_value[i][key])

                self.linear_coef[i][key] = popt
                self.linear_coef_std[i][key] = np.sqrt(np.diag(pcov))

    # returns dict
    # key - number of bearing
    # values : (pred, err, reason)
    # pred - predicted time in days from 2022.01.01 00:00
    # error - error in prediction in days
    # reason - Vibrations which would likely to cause fault
    def predict_linear(self):

        res = {}

        for i in BEARINGS_WITH_VIBS:

            for key in ['Vibration_horizntal', 'Vibration_vertical', 'Vibration_axis']:

                alarm_value =  self.data_alarm[i][key]

                pred = (alarm_value - self.linear_coef[i][key][1]) / self.linear_coef[i][key][0]
                err = np.sqrt( (pred  / self.linear_coef[i][key][0] \
                    * self.linear_coef_std[i][key][0])**2 + (self.linear_coef_std[i][key][1] / self.linear_coef[i][key][0])**2)

                if (i not in res.keys()) or res[i][0] >= pred:
                    res[i] = (pred, err, key)

        return res

    def trend_linear(self, x, key, ind):
        return self.linear_coef[ind][key][0] * x + self.linear_coef[ind][key][1]

