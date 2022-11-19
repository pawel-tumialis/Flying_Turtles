from numpy import load
import scipy.sparse

def read_weather(timestamp):
    #timestamp = '2022-07-06 00:37:25+00:00'
    #print(timestamp)
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

    file_name ='data/trajectory_challenge/VIL_merc/VIL_merc/VIL-' + timestamp + "-" + "{:02d}".format(hour) + '_' + "{:02d}".format(minute) + 'Z.npz'

    #print(file_name)

    sparse_matrix = scipy.sparse.load_npz(file_name)
    return sparse_matrix