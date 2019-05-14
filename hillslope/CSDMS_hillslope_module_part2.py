# This is a module to demonstrate how a model could be implemented in SedEdu
# The module is written and executed in Python


# import libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widget


# parameters
D = 50 # diffusivity
dt = 1
dx = 50


# set up the x and z arrays for the hillslope
x = np.arange(start=0, stop=1000, step=dx)
z = np.zeros(x.shape)
z[0:np.int(x.size/2)] = 100


# limits for the sliders
D_min = 0
D_max = 500


# setup the figure
plt.rcParams['toolbar'] = 'None' # turn off the matplotlib toolbar in the figure
plt.rcParams['figure.figsize'] = 5, 7 # size of the figure in inches

fig, ax = plt.subplots() # gives us a figure object and axes object to manipulate and plot things into
fig.subplots_adjust(left=0.15, bottom=0.3, top=0.95, right=0.9) # where do we want the limits of the axes object

fig.canvas.set_window_title('Hillslope model') # title of the figure window
ax.set_xlabel("x-distance") # the axis xlabel
ax.set_ylabel("elevation") # the axis ylabel
ax.set_ylim(0, 200) # the axis y limits
ax.set_xlim(x.min(), x.max())


# add plot elements
theline, = ax.plot(x, z, lw=1.5, color='blue')


# add slider
widget_color = 'lightgoldenrodyellow'

slide_ax = plt.axes([0.2, 0.1, 0.6, 0.05], facecolor=widget_color)
slide = widget.Slider(slide_ax, 'diffusivity', D_min, D_max, 
                      valinit=D, valstep=0.1, 
                      valfmt='%g', transform=ax.transAxes)

# show the results
plt.ion()

# preallocate vectors for consistency in size
sedflux_in = np.empty(x.shape, dtype=float)
sedflux_out = np.empty(x.shape, dtype=float)

while plt.fignum_exists(1):

    # read values from the slider
    D = slide.val

    # calculate slope and sediment flux
    rise = z[:-1] - z[1:]
    run = x[1:] - x[:-1]
    slope = rise / run
    q = slope * D # q is some dimensionless sediment flux, based just on slope and diffusivity    
    sedflux_out[0:-1] = q * dt

    # compute the sed flux into each cell
    sedflux_in[0] = 0
    sedflux_in[1:] = sedflux_out[:-1]

    # apply some boundary condition to define flux out of downstream cell
    sedflux_out[-1] = sedflux_out[-1] # zero-gradient boundary

    # compute the change in elevation per node
    dz = (sedflux_in - sedflux_out) / dx

    # update elevation
    z = z + dz

    # update the plot
    theline.set_ydata(z)

    plt.pause(0.001)
