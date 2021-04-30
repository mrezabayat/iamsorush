import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

import numpy as np
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

import os

cwd = os.getcwd()

# Read data sets
with cbook.get_sample_data(cwd+'/data.csv') as file:
    ab = np.loadtxt(file, delimiter=',', skiprows=1, max_rows=5, usecols=[0,1])
with cbook.get_sample_data(cwd+'/data.csv') as file:
    cd = np.loadtxt(file, delimiter=',', skiprows=1, max_rows=3, usecols=[3,4])

# scale b data
b_scale = 1

a = ab[:,0]
b = ab[:,1]*b_scale

c = cd[:,0]
d = cd[:,1]

# Print size of Data
print(ab.size)
print(cd.size)

# Font setup
# install latex for Ubuntu
# sudo apt-get install texlive-latex-extra texlive-fonts-recommended dvipng cm-super
# tex sample without latex   r'$a + \frac{\theta} {s}$'
plt.rc('text', usetex = True)
plt.rcParams["font.family"] = "monospace" # serif, sans-serif, monospace, cursive, fantasy
small_font = 10
medium_font = 12
big_font = 14

plt.rc('font', size=small_font)          # controls default text sizes
plt.rc('axes', titlesize=small_font)     # fontsize of the axes title
plt.rc('axes', labelsize=medium_font)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=small_font)    # fontsize of the tick labels
plt.rc('ytick', labelsize=small_font)    # fontsize of the tick labels
plt.rc('legend', fontsize=small_font)    # legend fontsize
plt.rc('figure', titlesize=big_font)  # fontsize of the figure title

# Plot
fig, ax = plt.subplots()
ax.plot(a, b, label='ab', linestyle='-', color='blue', linewidth=2)
ax.plot(c, d, label='cd', linestyle='none', marker="X", markersize=10,
         markeredgewidth=.5, markerfacecolor='orange', markeredgecolor='green' )

ax.legend()

ax.set_xlim([0,2])
ax.set_ylim([0.1,4])

# major tick step
ax.xaxis.set_major_locator(MultipleLocator(0.5))
ax.xaxis.set_major_formatter('{x:0.2f}')
# Divide a major step into 5 minor steps
ax.xaxis.set_minor_locator(AutoMinorLocator(5))
ax.grid()

plt.title('Graph', fontsize=big_font)
plt.xlabel('time', fontsize=medium_font)
plt.ylabel(r'$a + \frac{\theta} {s}$', fontsize=medium_font+0.5)
plt.yscale("linear") # "log", "symlog", "logit"
plt.show()

