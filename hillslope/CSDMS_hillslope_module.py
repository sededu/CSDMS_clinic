# This is a module to demonstrate how a model could be implemented in SedEdu
# The module is written and executed in Python


# IMPORT LIBLARIES
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widget


# SET PARAMETERS
D = 50 # diffusivity
U = 0
dt = 1
dx = 100

x = np.arange(start=0, stop=1000, step=dx)
z = np.zeros(x.shape)
z[0:np.floor(x.shape/2)] = 100


D_min = 0
D_max = 1000
U_max = 0.2
U_min = 0
C_max = 0.2
C_min = 0


# setup the figure
plt.rcParams['toolbar'] = 'None' # turn off the matplotlib toolbar in the figure
plt.rcParams['figure.figsize'] = 5, 7 # size of the figure in inches
plt.ion()

fig, ax = plt.subplots() # gives us a figure object and axes object to manipulate and plot things into
plt.subplots_adjust(left=0.2, bottom=0.4, top=0.95, right=0.9) # where do we want the limits of the axes object

fig.canvas.set_window_title('Hillslope model') # title of the figure window

ax.set_xlabel("x-distance") # the axis xlabel
ax.set_ylabel("elevation") # the axis ylabel
plt.ylim(0, 200) # the axis y limits


# add plot elements
theline, = plt.plot(x, z, lw=1.5, color='green')


# add slider
widget_color = 'lightgoldenrodyellow'

slide_D_ax = plt.axes([0.25, 0.25, 0.6, 0.05], facecolor=widget_color)
slide_D = widget.Slider(slide_D_ax, 'diffusivity', D_min, D_max, 
                               valinit=D, valstep=1, 
                               valfmt='%g', transform=ax.transAxes)

slide_U_ax = plt.axes([0.25, 0.15, 0.6, 0.05], facecolor=widget_color)
slide_U = widget.Slider(slide_U_ax, 'uplift at crest', U_min, U_max, 
                               valinit=U, valstep=0.001, 
                               valfmt='%g', transform=ax.transAxes)

slide_C_ax = plt.axes([0.25, 0.05, 0.6, 0.05], facecolor=widget_color)
slide_C = widget.Slider(slide_C_ax, 'downcut at valley', C_min, C_max, 
                               valinit=U, valstep=0.001, 
                               valfmt='%g', transform=ax.transAxes)

# # DEFINE FUNCTIONS
# def update(event):
#
#     # read values from the slider
#     them = slide.val 
#     # compute new y values
#     they = (them * x) + b
#     # update the plot
#     theline.set_ydata(they)
#     # redraw the canvas
#     fig.canvas.draw_idle()
#
# # connect widgets
# slide.on_changed(update)


# show the results
plt.show()

# preallocate vectors for consistency in size
sedflux_in = np.empty(x.shape, dtype=float)
sedflux_out = np.empty(x.shape, dtype=float)

cnt = 0
while plt.fignum_exists(1):

    D = slide_D.val

    # calculate slope and sediment flux
    rise = z[0:-1] - z[1:]
    run = x[1:] - x[:-1]
    slope = rise / run
    q = slope * -D # q is some dimensionless sediment flux, based just on slope and diffusivity    
    sedflux_out[0:-1] = -q * dt

    # compute the sed flux into each cell
    sedflux_in[0] = 0
    sedflux_in[1:] = sedflux_out[:-1]

    # apply some boundary condition to define flux out of downstream cell
    # sedflux_out[-1] = sedflux_in[-1] # zero-gradient downstream boundary
    sedflux_out[-1] = sedflux_out[-1] # zero-flux boundary?

    d_z = (sedflux_in - sedflux_out) / dx

    # apply boundary conditions
    d_z[0] = d_z[0] + slide_U.val
    d_z[-1] = d_z[-1] + -slide_C.val
    if z[-1] + d_z[-1] < 0:
        d_z[-1] = 0

    # update elevation
    z = z + d_z

    theline.set_ydata(z)

    plt.pause(0.001)
    cnt += 1
