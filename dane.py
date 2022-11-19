import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.sparse

def t_and_r(iter: int): #wyrzuca trajektorje i route dla i-tego indeksu z train_flights
    def router_usefull_data(file_):
        df = pd.read_csv(file_, sep=',')
        del df["code"]
        del df["type"]
        del df["seq_number"]
        return df

    train = pd.read_csv(f"../data/trajectory_challenge/train_flights.csv", sep=',')

    file_t = "../data/trajectory_challenge/train_trajectories/"+ train["id"][iter]  +".csv"
    file_r = "../data/trajectory_challenge/routes/"+ train["id"][iter]  +".csv"

    trajectories = pd.read_csv(file_t, sep=',')
    routes = router_usefull_data(file_r)

    return trajectories, routes

def read_weather(trajektorja, iter_in_tr):#wyrzuca pogode dla i-tego momentu w naszym ruchu
    text = trajektorja.track_timestamp[iter_in_tr]
    #timestamp = '2022-07-06 00:37:25+00:00'
    #print(timestamp)
    text = text[:text.find('+')]
    text = text[:text.rfind(':')]
    hour = int(text[text.rfind(':')-3:text.rfind(':')-1])
    minute = int(text[text.rfind(':')+1:text.rfind(':')+3])
    text = text[:text.rfind(' ')]
    if minute <= 15:
        minute = 0
    elif minute <= 45:
        minute = 30
    else:
        minute = 0
        hour += 1

    file_name ='../data/trajectory_challenge/VIL_merc/VIL-' + text + "-" + "{:02d}".format(hour) + '_' + "{:02d}".format(minute) + 'Z.npz'
    sparse_matrix = scipy.sparse.load_npz(file_name)
    return sparse_matrix