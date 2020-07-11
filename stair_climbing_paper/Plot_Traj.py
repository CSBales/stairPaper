import numpy as np
import matplotlib.pyplot as plt
from utilities import data, utilities


nb_states = 10
files = data.files
sides = data.sides
frames = data.frames
hills = utilities.get_index(frames, files, sides)

pathsZ, pathsY = utilities.make_toe(files, hills, sides)

f, (ax1, ax2) = plt.subplots(1, 2)
for pz, py in zip(pathsZ, pathsY):
    ax1.plot(pz)
    ax1.legend(['subj00', 'subj01', 'subj02', 'subj03', 'subj05', 'subj07', 'subj09', 'subj10'])
    ax2.plot(py)
    ax2.legend(['subj00', 'subj01', 'subj02', 'subj03', 'subj05', 'subj07', 'subj09', 'subj10'])

plt.show()
