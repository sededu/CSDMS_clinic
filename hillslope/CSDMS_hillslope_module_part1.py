# This is a module to demonstrate how a model could be implemented in SedEdu
# The module is written and executed in Python


# import liblaries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widget


# set parameters
m = 1
b = 0
x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y = (m * x) + b

mMax = 3
mMin = 0

# setup the figure
plt.rcParams['toolbar'] = 'None' # turn off the matplotlib toolbar in the figure
plt.rcParams['figure.figsize'] = 5, 7 # size of the figure in inches

fig, ax = plt.subplots() # gives us a figure object and axes object to manipulate and plot things into
fig.subplots_adjust(left=0.15, bottom=0.3, top=0.95, right=0.9) # where do we want the limits of the axes object

fig.canvas.set_window_title('demo') # title of the figure window
ax.set_xlabel("x") # the axis xlabel
ax.set_ylabel("y") # the axis ylabel
plt.ylim(-1, 31) # the axis y limits


# add plot elements
theline, = plt.plot(x, y, lw=1.5, color='blue')


# add slider
widget_color = 'lightgoldenrodyellow'

slide_ax = plt.axes([0.2, 0.1, 0.6, 0.05], facecolor=widget_color)
slide = widget.Slider(slide_ax, 'slope', mMin, mMax, 
                      valinit=m, valstep=0.1, 
                      valfmt='%g', transform=ax.transAxes)

# show the results
plt.ion()

while plt.fignum_exists(1):

    # read values from the slider
    them = slide.val

    # compute new y values
    they = (them * x) + b

    # update the plot
    theline.set_ydata(they)

    plt.pause(0.001)
