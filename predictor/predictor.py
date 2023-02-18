from scipy.optimize import curve_fit
import numpy as np
from datetime import datetime, timedelta
from statsmodels.tsa.holtwinters import ExponentialSmoothing

TEMP = [
    'SM_Exgauster\\[2:{}]'.format(27+i) for i in range(0, 9)
]

VIBR_HOR = [
    'SM_Exgauster\\[2:0]', 'SM_Exgauster\\[2:3]',
    'SM_Exgauster\\[2:6]', 'SM_Exgauster\\[2:9]'
]

VIBR_HOR_WARN = [
    'SM_Exgauster\\[2:161]', 'SM_Exgauster\\[2:164]',
    'SM_Exgauster\\[2:167]', 'SM_Exgauster\\[2:170]'
]

VIBR_VERT = [
    'SM_Exgauster\\[2:1]', 'SM_Exgauster\\[2:4]',
    'SM_Exgauster\\[2:7]', 'SM_Exgauster\\[2:10]'
]

VIBR_VERT_WARN = [
    'SM_Exgauster\\[2:162]', 'SM_Exgauster\\[2:165]',
    'SM_Exgauster\\[2:168]', 'SM_Exgauster\\[2:171]'
]

VIBR_AXIS = [
    'SM_Exgauster\\[2:2]', 'SM_Exgauster\\[2:5]',
    'SM_Exgauster\\[2:8]', 'SM_Exgauster\\[2:11]'
]

VIBR_AXIS_WARN = [
    'SM_Exgauster\\[2:163]', 'SM_Exgauster\\[2:166]',
    'SM_Exgauster\\[2:169]', 'SM_Exgauster\\[2:172]'
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

        self.data_warn = [{} for i in range(9)]

        self.linear_coef = [{} for i in range(9)]
        self.linear_coef_std = [{} for i in range(9)]

        self.hw_models = [{} for i in range(9)]
        self.hw_models_trend = [{} for i in range(9)]
        self.hw_models_trend_std = [{} for i in range(9)]

        for i in BEARINGS_WITH_VIBS:
            for key in ['Vibration_horizntal', 'Vibration_vertical', 'Vibration_axis']:
                self.linear_coef[i][key] = np.array([0, 0])
                self.linear_coef_std[i][key] = np.array([0, 0])

    def set_warn_val(self, key, ind, value):
        self.data_warn[ind][key] = value

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

            # add horizontal vibrations warning values
            for key, i in zip(iter(VIBR_HOR_WARN), [0, 1, 6, 7]):

                value = mes[key]
                if type(value) != float:
                    if 'Vibration_horizntal' in self.data_warn[i].keys():
                        value = self.data_warn[i]['Vibration_horizntal']
                    else:
                        value = 10.

                self.data_warn[i]['Vibration_horizntal'] = value

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

            # add vertical vibrations warning values
            for key, i in zip(iter(VIBR_VERT_WARN), [0, 1, 6, 7]):

                value = mes[key]
                if type(value) != float:
                    if 'Vibration_vertical' in self.data_warn[i].keys():
                        value = self.data_warn[i]['Vibration_vertical']
                    else:
                        value = 10.

                self.data_warn[i]['Vibration_vertical'] = value

            # add axis vibrations
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

            # add axis vibrations warning values
            for key, i in zip(iter(VIBR_AXIS_WARN), [0, 1, 6, 7]):

                value = mes[key]
                if type(value) != float:
                    if 'Vibration_axis' in self.data_warn[i].keys():
                        value = self.data_warn[i]['Vibration_axis']
                    else:
                        value = 10.

                self.data_warn[i]['Vibration_axis'] = value


    def fit_linear(self, n_days=np.inf):
        
        ind_start = 0

        for i in range(len(self.t)):
            if self.t[i] >= self.t[-1] - n_days:
                ind_start = i
                break

        for i in BEARINGS_WITH_VIBS:

            for key in ['Vibration_horizntal', 'Vibration_vertical', 'Vibration_axis']:

                popt, pcov = curve_fit(
                    linear,
                    self.t[ind_start:],
                    self.data_value[i][key][ind_start:])

                self.linear_coef[i][key] = popt
                self.linear_coef_std[i][key] = np.sqrt(np.diag(pcov))

    def fit_halt_winters(self, n_days=np.inf):

        ind_start = 0

        tmp = np.array(self.t)
        dt = np.mean(tmp[1:-1] - tmp[0:-2])

        for i in range(len(self.t)):
            if self.t[i] >= self.t[-1] - n_days:
                ind_start = i
                break

        period = round(2  / dt)
        N = round(20 / dt)

        for i in BEARINGS_WITH_VIBS:

            for key in ['Vibration_horizntal', 'Vibration_vertical', 'Vibration_axis']:
                x = self.data_value[i][key][ind_start:]
                self.hw_models[i][key] = ExponentialSmoothing(x, seasonal_periods=period, trend='add', seasonal='add').fit()

                pred = self.hw_models[i][key].predict(start=len(x), end=len(x)+N)
                t_pred = self.t[-1] + dt * (np.arange(N+1))

                popt, pcov = curve_fit(linear, t_pred, pred)

                self.hw_models_trend[i][key] = popt
                self.hw_models_trend_std[i][key] = np.diag(pcov) / 2

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

                alarm_value =  self.data_warn[i][key]

                pred = (alarm_value - self.linear_coef[i][key][1]) / self.linear_coef[i][key][0]
                err = np.sqrt( (pred  / self.linear_coef[i][key][0] \
                    * self.linear_coef_std[i][key][0])**2 + (self.linear_coef_std[i][key][1] / self.linear_coef[i][key][0])**2)

                if ((i not in res.keys()) or res[i][0] >= pred) \
                    and pred > (self.t[-1]-1):
                    res[i] = (pred, err, key)

        return res

    def build_hw(self, i, key, time):
        tmp = np.array(self.t)
        dt = np.mean(tmp[1:-1] - tmp[0:-2])
        N_start = len(self.t)
        N_end = round(time / dt) + N_start

        t_pred = self.t[-1]+dt* (np.arange(N_end-N_start+1))

        pred = self.hw_models[i][key].predict(start=N_start, end=N_end)

        return t_pred, pred - pred[0] + self.data_value[i][key][-1]

    def predict_hw(self):

        res = {}

        for i in BEARINGS_WITH_VIBS:

            for key in ['Vibration_horizntal', 'Vibration_vertical', 'Vibration_axis']:

                alarm_value =  self.data_warn[i][key]

                pred = (alarm_value - self.hw_models_trend[i][key][1]) / self.hw_models_trend[i][key][0]
                err = np.sqrt( (pred  / self.hw_models_trend[i][key][0] \
                    * self.hw_models_trend_std[i][key][0])**2 + (self.hw_models_trend_std[i][key][1] / self.hw_models_trend[i][key][0])**2)

                if ((i not in res.keys()) or res[i][0] >= pred) \
                    and pred > (self.t[-1]-1):
                    res[i] = (pred, err, key)

        return res

    def trend_linear(self, x, key, ind):
        return self.linear_coef[ind][key][0] * x + self.linear_coef[ind][key][1]

    def trend_hw(self, x, key, ind):
        return self.hw_models_trend[ind][key][0] * x + self.hw_models_trend[ind][key][1]
