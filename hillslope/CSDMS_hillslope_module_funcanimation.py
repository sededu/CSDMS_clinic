# This is a module to demonstrate how a model could be implemented in SedEdu
# The module is written and executed in Python


# import libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widget
import matplotlib.animation as animation

# add plot elements
def xz_to_fill(x, z):
    """
    this simple function provides a convenient way to calculate the polygon
    vertices for the hillslope from the x and z vectors.
    """
    x_fill = np.hstack([x, np.flipud(x)])
    z_fill = np.hstack([z, -np.ones(z.shape)])
    return x_fill, z_fill

class GUI(object):
    def __init__(self, hill):

        self.hill = hill

        # setup the figure
        plt.rcParams['toolbar'] = 'None' # turn off the matplotlib toolbar in the figure
        plt.rcParams['figure.figsize'] = 5, 7 # size of the figure in inches

        self.fig, self.ax = plt.subplots() # gives us a figure object and axes object to manipulate and plot things into
        self.fig.subplots_adjust(left=0.2, bottom=0.4, top=0.95, right=0.9) # where do we want the limits of the axes object

        self.fig.canvas.set_window_title('Hillslope model') # title of the figure window

        self.ax.set_xlabel("x-distance") # the axis xlabel
        self.ax.set_ylabel("elevation") # the axis ylabel
        self.ax.set_ylim(0, 200) # the axis y limits
        self.ax.set_xlim(hill.x.min(), hill.x.max())

        self.thesky, = self.ax.fill(np.array([-1, -1, hill.x.max(), hill.x.max()]),
                  np.array([-1, 250, 250, -1]), facecolor='aliceblue', edgecolor='none')
        # theline, = plt.plot(x, z, lw=1.5, color='green')
        x_fill, z_fill = xz_to_fill(hill.x, hill.z)
        self.thehill, = self.ax.fill(x_fill, z_fill, facecolor='forestgreen', edgecolor='k')

        self.thetext = self.ax.text(0.05, 0.05, '$dz/dt_{x=0}$' + '= {:.2f}'.format(hill.dzdt), transform=self.ax.transAxes)

        # add slider
        widget_color = 'lightgoldenrodyellow'

        self.slide_D_ax = plt.axes([0.2, 0.25, 0.4, 0.05], facecolor=widget_color)
        self.slide_D = widget.Slider(self.slide_D_ax, 'diffusivity', hill.D_min, hill.D_max, 
                                       valinit=hill.D, valstep=1, 
                                       valfmt='%g', transform=self.ax.transAxes)

        self.slide_U_ax = plt.axes([0.2, 0.15, 0.4, 0.05], facecolor=widget_color)
        self.slide_U = widget.Slider(self.slide_U_ax, 'uplift at\n crest', hill.U_min, hill.U_max, 
                                       valinit=hill.U, valstep=0.05, 
                                       valfmt='%g', transform=self.ax.transAxes)

        self.slide_C_ax = plt.axes([0.2, 0.05, 0.4, 0.05], facecolor=widget_color)
        self.slide_C = widget.Slider(self.slide_C_ax, 'downcut at\n valley', hill.C_min, hill.C_max, 
                                       valinit=hill.U, valstep=0.05, 
                                       valfmt='%g', transform=self.ax.transAxes)

        # btn_hill_reset_ax = plt.axes([0.7, 0.2, 0.25, 0.04])
        # btn_hill_reset = widget.Button(btn_hill_reset_ax, 'Reset hillslope', 
        #                                color=widget_color, hovercolor='0.975')

        # btn_slide_reset_ax = plt.axes([0.7, 0.1, 0.25, 0.04])
        # btn_slide_reset = widget.Button(btn_slide_reset_ax, 'Reset sliders', 
        #                                color=widget_color, hovercolor='0.975')


        # btn_hill_reset.on_clicked(reset_hillslope)
        # btn_slide_reset.on_clicked(reset_sliders)

        # show the results
        # plt.ion()


# reset functions
def reset_hillslope(event):
    z[:] = z_init[:]

def reset_sliders(event):
    slide_D.reset()
    slide_U.reset()
    slide_C.reset()
    fig.canvas.draw_idle()

# note that in this module, we have no update function, 
#   because we will continually update the plot in a while loop


class Hill(object):
    def __init__(self):

        # parameters
        self.D = 50 # diffusivity
        self.U = 0
        self.dt = 1
        self.dx = 50


        # set up the x and z arrays for the hillslope
        self.x = np.arange(start=0, stop=1000, step=self.dx)
        self.z = np.zeros(self.x.shape)
        self.z[0:np.int(self.x.size/2)] = 100
        self.z_init = self.z
        self.dzdt = 0


        # limits for the sliders
        self.D_min = 0
        self.D_max = 500
        self.U_max = 1
        self.U_min = 0
        self.C_max = 1
        self.C_min = 0

        # preallocate vectors for consistency in size
        self.sedflux_in = np.empty(self.x.shape, dtype=float)
        self.sedflux_out = np.empty(self.x.shape, dtype=float)


    def __call__(self,i):

        self.D = self.slide_D.val

        # calculate slope and sediment flux
        rise = self.z[0:-1] - self.z[1:]
        run = self.x[1:] - self.x[:-1]
        slope = rise / run
        q = slope * -self.D # q is some dimensionless sediment flux, based just on slope and diffusivity    
        self.sedflux_out[0:-1] = -q * self.dt

        # compute the sed flux into each cell
        self.sedflux_in[0] = 0
        self.sedflux_in[1:] = self.sedflux_out[:-1]

        # apply some boundary condition to define flux out of downstream cell
        self.sedflux_out[-1] = self.sedflux_out[-1] # zero-gradient boundary

        # compute the change in elevation per node
        dz = (self.sedflux_in - self.sedflux_out) / self.dx

        # apply boundary conditions
        dz[0] = dz[0] + self.slide_U.val
        dz[-1] = dz[-1] + -self.slide_C.val
        if self.z[-1] + dz[-1] < 0:
            dz[-1] = 0

        # update elevation
        self.z = self.z + dz
        dzdt = dz[0] / self.dt

        # update plot
        x_fill, z_fill = xz_to_fill(self.x, self.z)
        self.thehill.set_xy(np.row_stack([x_fill, z_fill]).transpose())
        self.thetext.set_text('$dz/dt_{x=0}$' + '= {:.2f}'.format(dzdt))

        # take a quick pause and bookeeping
        # plt.pause(0.001)
        # we now handle this pause with the "interval" defined in FuncAnimation

        return self.thehill

class Runner(object):
    def __init__(self):
        

        # time looping
        hill = Hill()
        gui = GUI(hill)

        hill.slide_D = gui.slide_D
        hill.slide_U = gui.slide_U
        hill.slide_C = gui.slide_C
        hill.thehill = gui.thehill
        hill.thetext = gui.thetext

        anim = animation.FuncAnimation(gui.fig, hill, 
                                       interval=10, blit=False,
                                       save_count=None)

        plt.show()



if __name__ == '__main__':
    runner = Runner()