import numpy as np
from GaitAnaylsisToolkit.LearningTools.Trainer import GMMTrainer
from GaitAnaylsisToolkit.Session import ViconGaitingTrial
from GaitAnaylsisToolkit.LearningTools.Runner import GMMRunner
from GaitCore.Core import Point
import matplotlib.pyplot as plt
from dtw import dtw
import numpy.polynomial.polynomial as poly


def make_toe(files, hills, sides):

    pathsZ = []
    pathsY = []

    for hill, file, side in zip(hills, files, sides):

        trial = ViconGaitingTrial.ViconGaitingTrial(vicon_file=file)
        marker = trial.vicon.get_markers()
        if side == "L":
            toe = marker.get_marker("LTOE")
        else:
            toe = marker.get_marker("RTOE")

        jointZ = []
        jointY = []

        for t in toe:
            jointZ.append(t.z)
            jointY.append(t.y)

        pathsZ.append(np.array([jointZ[h[0]] for h in hill]))
        pathsY.append(np.array([jointY[h[0]] for h in hill]))

    pathsZ[0] = pathsZ[0] - pathsZ[0][0]
    pathsZ[1] = pathsZ[1] - pathsZ[1][0]
    pathsZ[2] = pathsZ[2] - pathsZ[2][0]
    pathsZ[3] = pathsZ[3] - pathsZ[3][0]
    pathsZ[4] = pathsZ[4] - pathsZ[4][0]
    pathsZ[5] = pathsZ[5] - pathsZ[5][0]
    pathsZ[6] = pathsZ[6] - pathsZ[6][0]
    pathsZ[7] = pathsZ[7] - pathsZ[7][0]
    
    pathsY[0] = pathsY[0] - pathsY[0][0]
    pathsY[1] = pathsY[1] - pathsY[1][0]
    pathsY[2] = pathsY[2] - pathsY[2][0]
    pathsY[3] = pathsY[3] - pathsY[3][0]
    pathsY[4] = pathsY[4] - pathsY[4][0]
    pathsY[5] = pathsY[5] - pathsY[5][0]
    pathsY[6] = pathsY[6] - pathsY[6][0]
    pathsY[7] = pathsY[7] - pathsY[7][0]

    print(pathsZ[0])

    return pathsZ, pathsY


def get_index(frames, files, side):

    paths = []
    for file in files:
        trial = ViconGaitingTrial.ViconGaitingTrial(vicon_file=file)
        markers = trial.vicon.get_markers()
        markers.smart_sort()
        markers.auto_make_transform(frames)
        if side == "L":
            hills = trial.get_stairs("LTOE", "stairA")
        else:
            hills = trial.get_stairs("RTOE", "stairA")

        paths.append(hills[0])

    return paths
