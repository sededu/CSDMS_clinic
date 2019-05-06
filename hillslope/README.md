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

```
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

```
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
```
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
```
D = slide_D.val
```
and then we will swap out the computation for our 1-sided diffusion-like process simulation:

```


```

