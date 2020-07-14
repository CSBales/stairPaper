import numpy as np
import random
from scipy.optimize import curve_fit
from GaitAnaylsisToolkit.LearningTools.Trainer import GMMTrainer
from GaitAnaylsisToolkit.Session import ViconGaitingTrial
from GaitAnaylsisToolkit.LearningTools.Runner import GMMRunner
from GaitCore.Core import Point
import matplotlib.pyplot as plt
import pickle
from dtw import dtw
from utilities import data, utilities
import numpy.polynomial.polynomial as poly


files = data.files
sides = data.sides
frames = data.frames
hills = utilities.get_index(frames, files, sides)

pathsZ, pathsY = utilities.make_toe(files, hills, sides)


def calculate_imitation_metric_1(demos, imitation):
    M = len(demos)
    T = len(imitation)
    imitation = np.array(imitation)
    metric = 0.0
    paths = []
    t = []
    t.append(1.0)
    alpha = 1.0
    manhattan_distance = lambda x, y: abs(x - y)

    for i in range(1, T):
        t.append(t[i - 1] - alpha * t[i - 1] * 0.01)  # Update of decay term (ds/dt=-alpha s) )
    t = np.array(t)

    for m in range(M):
        d, cost_matrix, acc_cost_matrix, path = dtw(imitation, demos[m], dist=manhattan_distance)
        data_warp = [demos[m][path[1]][:imitation.shape[0]]]
        coefs = poly.polyfit(t, data_warp[0], 20)
        ffit = poly.Polynomial(coefs)
        y_fit = ffit(t)
        paths.append(y_fit)
        metric += np.sum(abs(y_fit - imitation.flatten()))

    return paths, metric/(M*T)

# runner_toeZ = make_toeZ(filesZ, hillsZ, nb_states, "toeZ_all2")
# runner_toeY = make_toeY(filesY, hillsY, nb_states, "toeY_all")

# runnerY = GMMRunner.GMMRunner("toeY_all" + ".pickle")
# runnerZ = GMMRunner.GMMRunner("toeZ_all1" + ".pickle")
#
# imitationY = runnerY.run()
# imitationZ = runnerZ.run()


metricsZ = []
metricsY = []

for i in range(1, len(pathsZ)+1):

    sample_set = random.sample(range(len(pathsZ)), i)
    pathsZ_partial = []

    for k in sample_set:
        pathsZ_partial.append(pathsZ[k])

    trainerZ = GMMTrainer.GMMTrainer(pathsZ_partial, "toeZ_all" + str(i), 6, 0.01)
    trainerZ.train()
    runnerZ = GMMRunner.GMMRunner("toeZ_all" + str(i) + ".pickle")
    imitationZ = runnerZ.run()
    pathZ, metric = calculate_imitation_metric_1(pathsZ_partial, imitationZ)
    metricsZ.append([i, metric])

for i in range(1, len(pathsY)+1):

    sample_set = random.sample(range(len(pathsY)), i)
    pathsY_partial = []

    for k in sample_set:
        pathsY_partial.append(pathsY[k])

    trainerY = GMMTrainer.GMMTrainer(pathsY_partial, "toeY_all" + str(i), 10, 0.01)
    trainerY.train()
    runnerY = GMMRunner.GMMRunner("toeY_all" + str(i) + ".pickle")
    imitationY = runnerY.run()
    pathY, metric = calculate_imitation_metric_1(pathsY_partial, imitationY)
    metricsY.append([i, metric])

plt.rcParams.update({'font.size': 22})
fig0, ax0 = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(5, 3))
fig1, ax1 = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(5, 3))
fig2, ax2 = plt.subplots(nrows=1, ncols=1, figsize=(5, 3))
fig3, ax3 = plt.subplots(nrows=1, ncols=1, figsize=(5, 3))

metricsY = np.array(metricsY)
metricsZ = np.array(metricsZ)

ax0.set_xlim(0, 10)
ax1.set_xlim(0, 10)
ax0.plot(metricsY[:, 0], metricsY[:, 1], "-o")
ax1.plot(metricsZ[:, 0], metricsZ[:, 1], "-o")


# def func(x, a, b, c):
#     return a * np.exp(-b * x) + c


# poptY, pcovY = curve_fit(func, metricsY[:, 0], metricsY[:, 1], p0=(1, 4, 1))
# poptZ, pcovZ = curve_fit(func, metricsZ[:, 0], metricsZ[:, 1], p0=(1, 4, 1))
# ax0.plot(metricsY[:, 0], func(metricsY[:, 0], *poptY))
# ax1.plot(metricsZ[:, 0], func(metricsZ[:, 0], *poptZ))

ax0.set_title("Y Imitation cost")
ax1.set_title("Z Imitation cost")
ax0.set_xlabel("K")
ax1.set_xlabel("K")
ax0.set_ylabel("Cost")
ax1.set_ylabel("Cost")
ax0.grid()
ax1.grid()

for p in pathY:
    ax2.plot(p)

for p in pathZ:
    ax3.plot(p)

ax2.set_title("Y Imitation Comparison")
ax3.set_title("Z Imitation Comparison")
ax2.plot(imitationY, linewidth=3)
ax3.plot(imitationZ, linewidth=3)

ax2.set_title("Y Trajectories")
ax3.set_title("Z Trajectories")

ax2.legend(["1", "2", "3", "4", "5", "6", "7", "8", "Learned"])
ax3.legend(["1", "2", "3", "4", "5", "6", "7", "8", "Learned"])

ax2.set_xlabel("Frame")
ax2.set_ylabel("Position (mm)")
ax3.set_xlabel("Frame")
ax3.set_ylabel("Position (mm)")

plt.show()
