import folium
import numpy as np
from numpy import load
from scipy import sparse
import pandas as pd

weather_name = ''
path_to_train ='D:/Projects\Heckathon/trajectory_challenge/train_flights.csv'
fmap = folium.Map(location=[35, -100], zoom_start=6)

BOUNDARIES = [(21.9430, -67.5), (55.7765, -135)]
VIL_THRESHOLD_COLORS = [
    (10000, (0.63, 0.0, 0.01, 1.0)),
    (32.32, (0.87, 0.56, 0.0, 1.0)),
    (12.16, (0.95, 0.75, 0.0, 1.0)),
    (7.08, (0.93, 0.95, 0.0, 1.0)),
    (3.53, (0.38, 0.69, 0.0, 1.0)),
    (0.77, (0.63, 0.94, 0.0, 1.0)),
    (0.52, (0.9, 0.9, 0.9, 0.03)),
]

def _matrix_to_weather_colormap(sparse_matrix: sparse.csr_matrix) -> np.ndarray:
    matrix = sparse_matrix.toarray()
    result = np.zeros(shape=matrix.shape + (4,))
    for thresh, color in VIL_THRESHOLD_COLORS:
        result[matrix <= thresh] = color
    return result

def _plot_matrix(sparse_matrix: sparse.csr_matrix) -> folium.Map:
    colored_matrix = _matrix_to_weather_colormap(sparse_matrix=sparse_matrix)

    folium.raster_layers.ImageOverlay(
        colored_matrix,
        pixelated=True,
        opacity=0.8,
        mercator_project=True,
        bounds=BOUNDARIES,
    ).add_to(fmap)
    return fmap

def router_usefull_data(trajektoria: str):
    df = pd.read_csv(trajektoria, sep=',')
    del df["code"]
    del df["type"]
    del df["seq_number"]
    return df

def load_and_show_vil(pogoda: str, trajektoria: str) -> folium.Map:
    sparse_matrix = sparse.load_npz(pogoda)
    plot = _plot_matrix(sparse_matrix=sparse_matrix)

    df = router_usefull_data(trajektoria)
    route = df.to_numpy()
    for i in range(len(route)):
        folium.Marker(location=[route[i,0],route[i,1]]).add_to(fmap)
        
    
    return plot

def read_weather_name(timestamp):
    timestamp = timestamp[:timestamp.find('+')]
    timestamp = timestamp[:timestamp.rfind(':')]
    hour = int(timestamp[timestamp.rfind(':')-3:timestamp.rfind(':')-1])
    minute = int(timestamp[timestamp.rfind(':')+1:timestamp.rfind(':')+3])
    timestamp = timestamp[:timestamp.rfind(' ')]
    if minute <= 15:
        minute = 0
    elif minute <= 45:
        minute = 30
    else:
        minute = 0
        hour += 1
    file_name ='trajectory_challenge/VIL_merc/VIL-' + timestamp + "-" + "{:02d}".format(hour) + '_' + "{:02d}".format(minute) + 'Z.npz'
    return file_name

load_and_show_vil(f"D:/Projects/Heckathon/trajectory_challenge/VIL_merc/VIL-2022-07-01-00_00Z.npz", f"D:/Projects/Heckathon/trajectory_challenge/routes/flp_2A7i5CZ7tLiLnKGKgUeNFY.csv")