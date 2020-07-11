import numpy as np
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

for i in range(2, 25):
    runnerZ = GMMRunner.GMMRunner("toeZ_all" + str(i) + ".pickle")
    imitationZ = runnerZ.run()
    pathZ, metric = calculate_imitation_metric_1(pathsZ, imitationZ)
    metricsZ.append([i, metric])

for i in range(2, 25):
    runnerY = GMMRunner.GMMRunner("toeY_all" + str(i) + ".pickle")
    imitationY = runnerY.run()
    pathY, metric = calculate_imitation_metric_1(pathsY, imitationY)
    metricsY.append([i, metric])

plt.rcParams.update({'font.size': 22})
fig2, ax2 = plt.subplots(nrows=1, ncols=2, figsize=(5, 3))
fig1, ax1 = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(5, 3))

metricsY = np.array(metricsY)
metricsZ = np.array(metricsZ)

ax1[0].plot(metricsY[:, 0], metricsY[:, 1], "-o")
ax1[1].plot(metricsZ[:, 0], metricsZ[:, 1], "-o" )
ax1[0].set_title("Y Imitation cost")
ax1[1].set_title("Z Imitation cost")
fig1.suptitle("Imitation cost")
ax1[1].set_xlabel("K")
ax1[0].set_ylabel("cost")
ax1[1].set_ylabel("cost")

for p in pathY:
    ax2[0].plot(p)

for p in pathZ:
    ax2[1].plot(p)

fig2.suptitle("Imitation Comparison")
ax2[0].plot(imitationY, linewidth=3)
ax2[1].plot(imitationZ, linewidth=3)

ax2[1].set_title("Z Trajectories")
ax2[0].set_title("Y Trajectories")

ax2[1].legend(["file00", "file01", "file02", "file03", "file05", "file07", "file09", "file10", "Learned Model"])
ax2[0].legend(["file00", "file01", "file02", "file03", "file05", "file07", "file09", "file10", "Learned Model"])

ax2[0].set_xlabel("s")
ax2[0].set_ylabel("pos (mm)")
ax2[1].set_xlabel("s")
ax2[1].set_ylabel("pos (mm)")

plt.show()
