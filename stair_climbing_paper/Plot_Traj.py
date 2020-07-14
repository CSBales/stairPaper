import numpy as np
import matplotlib.pyplot as plt
from utilities import data, utilities


nb_states = 10
files = data.files
sides = data.sides
frames = data.frames
hills = utilities.get_index(frames, files, sides)

pathsZ, pathsY = utilities.make_toe(files, hills, sides)

f, (ax1, ax2) = plt.subplots(2, 1)
for pz, py in zip(pathsZ, pathsY):
    ax1.plot(pz)
    ax1.legend(['subject 00', 'subject 01', 'subject 02', 'subject 03', 'subject 05',
                'subject 07', 'subject 09', 'subject 10'])
    ax1.set_xlabel("Frame")
    ax1.set_ylabel("Position (mm)")
    ax1.set_title("Z-Position")
    ax2.plot(py)
    ax2.legend(['subject 00', 'subject 01', 'subject 02', 'subject 03', 'subject 05',
                'subject 07', 'subject 09', 'subject 10'])
    ax2.set_xlabel("Frame")
    ax2.set_ylabel("Position (mm)")
    ax2.set_title("Y-Position")

    f.suptitle("Trained Trajectories")

plt.show()
