import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.sparse

def t_and_r(iter: int):
    def router_usefull_data(file_):
        df = pd.read_csv(file_, sep=',')
        del df["code"]
        del df["type"]
        del df["seq_number"]
        return df

    train = pd.read_csv(f"../data/trajectory_challenge/train_flights.csv", sep=',')

    file_t = "../data/trajectory_challenge/train_trajectories/"+ train["id"][iter]  +".csv"
    file_r = "../data/trajectory_challenge/routes/"+ train["id"][iter]  +".csv"

    #2k x i 2k y routes 30
    trajectories = pd.read_csv(file_t, sep=',')
    routes = router_usefull_data(file_r)

    no_t = trajectories["lon"].count()
    no_r = routes["lon"].count()
    
    row = [trajectories.iloc[no_t-1][0], trajectories.iloc[no_t-1][1], trajectories.iloc[no_t-1][2]]
    print(row)
    row_ = row.copy()            
    if(no_t < 2000):        #duplikowanie trajektorii
        for i in range(no_t, 2000):
            trajectories.loc[i] = row_     
    else:
        s = np.arange(no_t-2000)
        ind = (1/(no_t-2000+1)*no_t)*s
        ind = ind.astype(int)
        trajectories = trajectories.drop(trajectories.index[ind])
        trajectories = trajectories.reset_index(drop=True)
    
    row = [routes.iloc[no_r-1][0], routes.iloc[no_r-1][1]]
    #print(row)
    row_ = row.copy()  
    if(no_r < 5):        #duplikowanie routsow
        for i in range(no_r, 35):
            routes.loc[i] = row_      
    else:
        s = np.arange(no_r-35)
        ind = (1/(no_r-35+1)*no_r)*s
        ind = ind.astype(int)
        routes = routes.drop(routes.index[ind])
        routes = routes.reset_index(drop=True)
    
    return trajectories, routes

def read_weather(trajektorja, iter_in_tr):
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