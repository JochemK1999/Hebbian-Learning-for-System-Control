import matplotlib.pyplot as plt
import numpy as np

methods = [None, 'none', 'nearest', 'bilinear', 'bicubic', 'spline16',
           'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
           'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos']

COMBINATIONS = False

grid = np.load("network.npy")

x_ticks = [0, 1, 2]
x_labels = ["nothing", "jump", "long_jump"] #"duck",
y_ticks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
y_lables = ["d1_1", "d2_1", "d3_1", "d4_1", "d5_1", "d6_1", "d1_2", "d2_2", "d3_2", "d4_2", "d5_2", "d6_2", "d1_3", "d2_3", "d3_3", "d4_3", "d5_3", "d6_3"]

if COMBINATIONS:
    index = 0
    for i in range(6):
        for j in range(i+1, 6):
            y_ticks.append(len(y_ticks))
            y_lables.append(f"{y_lables[i]}*{y_lables[j]}")


plt.imshow(grid[:, [0, 1, 2]], aspect='auto', interpolation='none')
plt.xticks(x_ticks, x_labels)
plt.yticks(y_ticks, y_lables)
plt.colorbar()
plt.show()


