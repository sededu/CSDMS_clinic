# CSDMS clinic instructions for hillslope diffusion module

## starting with the `interactive_gui_demo.py` file

Let's start from the file we just stepped through, and work from there. 
In your folder `CSDMS_clinic` is a bunch of `.py` files with names `CSDMS_hillslope_module_***.py`.
These are all checkpoints in the progression through the steps in this document.

Start with `CSDMS_hillslope_module_part0.py`; this is a nearly exact copy of the `interactive_gui_demo.py` that we just stepped through.
"Save as" your file to something similar, with your name (e.g., `moodie_CSDMS_hillslope_module.py`).

## Part 1 -- the `while` loop

The first thing we need to do is change the structure of the code so that the figure is updated regularly, without intervention from the user.
We'll use a `while` loop to accomplish this. 
If this doesn't mean anything to you, that's fine, a `while` loop is a sequence of commands the the computer is told to execute repeatedly until some condition is _no longer true_.

Our `while` loop will be based on the condition that the `Figure` object exists; so while the figure exists, we will continue to execute the code.
At the end of the code, type or copy-paste the following.

```python
while plt.fignum_exists(1):

    # read values from the slider
    them = slide.val

    # compute new y values
    they = (them * x) + b

    # update the plot
    theline.set_ydata(they)

    plt.pause(0.001)
```

This should look familiar to you -- it is very similar to the `update` function we used in the example module. 
Let's go ahead and delete all the code making up the `update` function, as well as the connection to the slider.
Replace the `plt.show()` line with `plt.ion()`.
Go ahead and rerun this new code.

You should see the same functionality as we previously established, but we have set things up differently. 
In this formulation, every loop we grab the value of the slider and do our calculation based on the slope -- whether the value is changed or the same.


## Part 2 -- creating a hillslope

In this part, we will change our simple model of a sloping line, into a hillslope which evolves by a diffusion process.
Change the name of the parameters to keep with the diffusion equation and a hillslope.

```python
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
```

We are also going to change the "window title", axis labels, and axis limits in this step.
```python
fig.canvas.set_window_title('Hillslope model') # title of the figure window
ax.set_xlabel("x-distance") # the axis xlabel
ax.set_ylabel("elevation") # the axis ylabel
ax.set_ylim(0, 200) # the axis y limits
ax.set_xlim(x.min(), x.max())
```

Update the plotting command so that we are plotting `z` instead of `y`.

Update the slider to the appropriate "label", initial value, and limits we defined as parameters.

### the only science we're going to do today

Now we need to add the only small bit of science we're going to do today to the module.
We're going to simulate hillslope evolution with a diffusion-like process, where the elevation-slope is the driving gradient.

As far as the module is concerned, we're not really changing anything here; the workflow is still to 1) read the slider value 2) do some computation with this value, and 3) update the plot.

So let's fix the variable name we grab from the slider:
```python
D = slide_D.val
```
and then we will swap out the computation for our 1-sided diffusion-like process simulation:

```python
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

# update elevation
z = z + dz

# update the plot
theline.set_ydata(z)
```

That's the bulk of the change to make this an interactive geomorphology / sedimentology activity. 
We can (and will) continue to add features to the module, but this hopefully gives you a sense of how things work.


## Part 3 -- adding buttons and sliders
 
The module we have developed thus far is nice, but we want to be able to teach students about more than just a diffusion-like morphology.
Let's work on adding some more features. 

__At this point, I encourage you to explore developing on your own; what feature would you like to see implemented?__

I will walk through how to add two "reset" buttons now, and how to add additional sliders. I will set up my sliders to control the elevation change at the boundaries, but you could make your do anything else instead.

### adding sliders
First, let's make some space to add more sliders and some buttons.
We need to adjust the layout of the subplots to do this.
I'm also going to rename my slider to make it unambiguous which sliders are linked to which model controls.

Shift the plot window up a bit, and the slider right edge to the left a bit:
```python
fig.subplots_adjust(left=0.2, bottom=0.4, top=0.95, right=0.9)
```
```python
slide_D_ax = plt.axes([0.2, 0.25, 0.4, 0.05], facecolor=widget_color)
slide_D = widget.Slider(slide_D_ax, 'diffusivity', D_min, D_max, 
                               valinit=D, valstep=1, 
                               valfmt='%g', transform=ax.transAxes)
```
(don't forget to also change the reference to the slider in the `while` loop!)

Below I'm going to put the components I have used to make a slider which controls the uplift rate at the crest of the hillslope. Place them in the correct places in the code to make the slider work.

```python
slide_U_ax = plt.axes([0.2, 0.15, 0.4, 0.05], facecolor=widget_color)
slide_U = widget.Slider(slide_U_ax, 'uplift at\n crest', U_min, U_max, 
                               valinit=U, valstep=0.001, 
                               valfmt='%g', transform=ax.transAxes) 
```
```python
dz[0] = dz[0] + slide_U.val
```
```python
U = 0
U_max = 0.4
U_min = 0
```

Try and add a slider which controls the downcutting rate at the downstream end. 
How would you prevent the elevation from going below 0?

You can see how I implemented this in `CSDMS_hillslope_module_part3.py`, but try it on your own!

### adding reset buttons

The process for creating a button is _very_ similar to the process we used to connect a slider in the previous tutorial with the sloping line.
Let's first make a button that resets the sliders to their initial values.
This uses the `Button` class from `matplotlib`:
```python
btn_slide_reset_ax = plt.axes([0.7, 0.1, 0.25, 0.04])
btn_slide_reset = widget.Button(btn_slide_reset_ax, 'Reset sliders', 
                               color=widget_color, hovercolor='0.975')
```

Now we need a function to execute each time out button is pushed:
```python
# reset functions
def reset_sliders(event):
    slide_D.reset()
    slide_U.reset()
    slide_C.reset()
    fig.canvas.draw_idle()
```
(be sure the names of the sliders in the reset function match the slider names in your code!)

And finally, we need to connect the button to the function 
```python
btn_slide_reset.on_clicked(reset_sliders)
```

Try and run your script, and test the reset button.

Try and implement a button to reset the hillslope.
You can see my implementation of this in the `CSDMS_hillslope_module_part3.py` file.


## Part 4 -- dressing it up a bit
That wraps up the mechanics of the module!
What follows will be a few tricks on making your module a little more visually appealing.
In my experience, these final steps in polishing the presentation really make a difference in student comprehension--it pays for your module to _look like_ the thing you are emulating.

To do this, we'll add a sky background, and make the hillslope green.
Finally, we'll add a meter for the rate of change of elevation at the crest.












## Part 5 -- some notes
This tutorial does not explain a few important parts of getting your module into SedEdu.
That information can be found here:

Also, this method of using a `while` loop is not _exactly_ the correct way to do things.
The problem with this approach is that the window always demands to be "on top".
This would be really troublesome for student trying to work through and activity on their computers at the same time.

`matplotlib` provides a better way to do the same thing, but the process is a little more involved and requires a deeper comprehension of Python classes and objects. 
I hope to write my own tutorial eventually about how to use the `funcanimation` tool (LINK HERE), but for now you can utilize `matplotlibs`'s documentation, or look at the rivers2stratigraphy activity for an example of how the tool works.