import numpy as np
import matplotlib.pyplot as plt
from utilities import data, utilities
from GaitAnaylsisToolkit.LearningTools.Trainer import GMMTrainer


files = data.files
sides = data.sides
frames = data.frames
hills = utilities.get_index(frames, files, sides)
pathsZ, pathsY = utilities.make_toe(files, hills, sides)

output = []
min_values = []
min_scores = []
all_x = []
all_y = []


for i in range(2, 25):
    trainer = GMMTrainer.GMMTrainer(pathsZ, "name", i, 0.01)
    bic = trainer.train(save=False)
    output.append([i, bic])

x = []
y = []
for o in output:
    x.append(o[0])
    y.append(o[1]["BIC"])

all_x.append(x)
all_y.append(y)
plt.plot(x, y)


plt.ylabel("BIC_score")
plt.xlabel("K")
plt.title("BIC score (smaller is better)")
x = np.mean(all_x, axis=0).tolist()
y = np.mean(all_y, axis=0).tolist()


plt.plot(x, y, c="k", linewidth=3)
plt.show()
