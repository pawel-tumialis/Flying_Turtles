import numpy as np
import tensorflow as ts
import matplotlib as plt
import pandas as pd
from scipy import sparse
import folium
from pathlib import Path  

file  = "D:/Projects/Heckathon/testy/input/flp_2A2CLJ5truHZphTggebR4K.csv"

def router_usefull_data(file_):
    df = pd.read_csv(file_, sep=',')
    del df["code"]
    del df["type"]
    del df["seq_number"]
    return df

#print(router_usefull_data(file))
