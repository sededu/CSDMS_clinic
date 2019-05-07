# This is a module to demonstrate how a model could be implemented in SedEdu
# The module is written and executed in Python


# import libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widget


# parameters
D = 50 # diffusivity
U = 0
dt = 1
dx = 50


# set up the x and z arrays for the hillslope
x = np.arange(start=0, stop=1000, step=dx)
z = np.zeros(x.shape)
z[0:np.int(x.size/2)] = 100
z_init = z


# limits for the sliders
D_min = 0
D_max = 500
U_max = 1
U_min = 0
C_max = 1
C_min = 0


# setup the figure
plt.rcParams['toolbar'] = 'None' # turn off the matplotlib toolbar in the figure
plt.rcParams['figure.figsize'] = 5, 7 # size of the figure in inches

fig, ax = plt.subplots() # gives us a figure object and axes object to manipulate and plot things into
fig.subplots_adjust(left=0.2, bottom=0.4, top=0.95, right=0.9) # where do we want the limits of the axes object

fig.canvas.set_window_title('Hillslope model') # title of the figure window
ax.set_xlabel("x-distance") # the axis xlabel
ax.set_ylabel("elevation") # the axis ylabel
ax.set_ylim(0, 200) # the axis y limits
ax.set_xlim(x.min(), x.max())


# add plot elements
theline, = plt.plot(x, z, lw=1.5, color='blue')


# add slider
widget_color = 'lightgoldenrodyellow'

slide_D_ax = plt.axes([0.2, 0.25, 0.4, 0.05], facecolor=widget_color)
slide_D = widget.Slider(slide_D_ax, 'diffusivity', D_min, D_max, 
                               valinit=D, valstep=1, 
                               valfmt='%g', transform=ax.transAxes)

slide_U_ax = plt.axes([0.2, 0.15, 0.4, 0.05], facecolor=widget_color)
slide_U = widget.Slider(slide_U_ax, 'uplift at\n crest', U_min, U_max, 
                               valinit=U, valstep=0.05, 
                               valfmt='%g', transform=ax.transAxes)

slide_C_ax = plt.axes([0.2, 0.05, 0.4, 0.05], facecolor=widget_color)
slide_C = widget.Slider(slide_C_ax, 'downcut at\n valley', C_min, C_max, 
                               valinit=U, valstep=0.05, 
                               valfmt='%g', transform=ax.transAxes)

btn_hill_reset_ax = plt.axes([0.7, 0.2, 0.25, 0.04])
btn_hill_reset = widget.Button(btn_hill_reset_ax, 'Reset hillslope', 
                               color=widget_color, hovercolor='0.975')

btn_slide_reset_ax = plt.axes([0.7, 0.1, 0.25, 0.04])
btn_slide_reset = widget.Button(btn_slide_reset_ax, 'Reset sliders', 
                               color=widget_color, hovercolor='0.975')

# reset functions
def reset_hillslope(event):
    z[:] = z_init[:]

def reset_sliders(event):
    slide_D.reset()
    slide_U.reset()
    slide_C.reset()
    fig.canvas.draw_idle() 

btn_hill_reset.on_clicked(reset_hillslope)
btn_slide_reset.on_clicked(reset_sliders)

# show the results
plt.ion()

# preallocate vectors for consistency in size
sedflux_in = np.empty(x.shape, dtype=float)
sedflux_out = np.empty(x.shape, dtype=float)

while plt.fignum_exists(1):

    # read values from the slider
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
    sedflux_out[-1] = sedflux_out[-1] # zero-gradient boundary

    # compute the change in elevation per node
    dz = (sedflux_in - sedflux_out) / dx

    # apply boundary condition updates
    dz[0] = dz[0] + slide_U.val
    dz[-1] = dz[-1] + -slide_C.val
    if z[-1] + dz[-1] < 0:
        dz[-1] = 0

    # update elevation
    z = z + dz

    # update the plot
    theline.set_ydata(z)

    plt.pause(0.001)
