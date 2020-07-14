import numpy as np
import matplotlib.pyplot as plt
from utilities import data, utilities
from GaitAnaylsisToolkit.LearningTools.Trainer import GMMTrainer


files = data.files
sides = data.sides
frames = data.frames
hills = utilities.get_index(frames, files, sides)
pathsZ, pathsY = utilities.make_toe(files, hills, sides)

outputZ = []
outputY = []
min_values = []
min_scores = []
all_Zx = []
all_Zy = []
all_Yx = []
all_Yy = []

for i in range(2, 25):
    trainer = GMMTrainer.GMMTrainer(pathsZ, "name", i, 0.01)
    bic = trainer.train(save=False)
    outputZ.append([i, bic])
for i in range(2, 25):
    trainer = GMMTrainer.GMMTrainer(pathsY, "name", i, 0.01)
    bic = trainer.train(save=False)
    outputY.append([i, bic])

Zx = []
Zy = []
Yx = []
Yy = []

for o in outputZ:
    Zx.append(o[0])
    Zy.append(o[1]["BIC"])
for o in outputY:
    Yx.append(o[0])
    Yy.append(o[1]["BIC"])

all_Zx.append(Zx)
all_Zy.append(Zy)
all_Yx.append(Yx)
all_Yy.append(Yy)

f1, ax1 = plt.subplots(1, 1)
f2, ax2 = plt.subplots(1, 1)
ax1.plot(Zx, Zy)
ax2.plot(Yx, Yy)

ax1.set_xlabel("K")
ax1.set_ylabel("BIC score")
ax1.set_title("Z BIC score")
ax2.set_xlabel("K")
ax2.set_ylabel("BIC score")
ax2.set_title("Y BIC score")

Zx = np.mean(all_Zx, axis=0).tolist()
Zy = np.mean(all_Zy, axis=0).tolist()
ax1.plot(Zx, Zy, c="k", linewidth=3)
ax1.grid()

Yx = np.mean(all_Yx, axis=0).tolist()
Yy = np.mean(all_Yy, axis=0).tolist()
ax2.plot(Yx, Yy, c="k", linewidth=3)
ax2.grid()

plt.show()
