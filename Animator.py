from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import colormaps, rcParams
from matplotlib.colors import ListedColormap, Normalize

class Animator:
    """
    A class to animate simulations in 2D.
    Used together with Plotter.
    """

    def __init__(self, update, init=(lambda: None), interval=100, save=False, fps=None, frames=None, name='simulation'):
        """
        Initializes the necessary attributes for an Animator object.

        Args
        ----
        update: func
            Updates the state of the simuation.
        init: func, optional
            Init function for the simulation animation, e.g. for drawing
            the initial state of the simulation.  Default is None.
        interval: int, optional
            Time between redrawing. Default is 100.
        save: bool, optional
            Whether or not to save the animation as an mp4 file. 
            Default is False.
        fps: int, optional
            Playback speed for the saved animation.
            Default is None.
        frames: int, optional
            How many frames of the animation to run. Default is None.
            If save == True, frames attribute needs to be set to some value, 
            othewise the program will try to save an infinitely long animation.
        name: str, optional
            The name/path of the animation you wish to save. 
            Default is "simulation". 
        """

        self.update = update
        self.interval = interval
        self.init = init
        self.running = True
        self.save = save
        self.fps = fps
        self.cache_frame_data =  True
        self.frames = frames
        if self.frames is None:
            self.cache_frame_data = False
            if self.save:
                raise AttributeError("Need to set frames attribute.")
        self.name = name
        self.fig = plt.figure()
        self.fig.canvas.manager.set_window_title('Animator')
        plt.gca().get_xaxis().set_visible(False)
        plt.gca().get_yaxis().set_visible(False)

    def animate(self):
        """
        Animates the simulation. 

        Returns
        -------
        None
        """

        def on_click(e):
            """
            Pauses the animation when pressing space. 
            """
            if anim.event_source is None:
                return
            
            if e.key.isspace():
                if self.running:
                    anim.event_source.stop()
                    self.running = False
                else:
                    anim.event_source.start()
                    self.running = True

        self.fig.canvas.mpl_connect('key_press_event', on_click)
        anim = FuncAnimation(self.fig, self.update, init_func=self.init,
                             frames=self.frames, cache_frame_data=self.cache_frame_data,
                             interval=self.interval, repeat=False)
        if self.save:
            print("Rendering video...")
            anim.save(self.name + '.mp4', writer='ffmpeg', fps=self.fps) 
        else:
            plt.show()

class Plotter:
    """
    A class to plot simulations in  2D.
    Used together with Animator.
    """
    def __init__(self, standard=None, custom=None):
        """
        Initializes the necessary attributes for a Plotter object.

        Args
        ----
        standard: str, optional
            Name of a built-in Matplotlib colormap. Default is None. 
        custom: Colormap, optional
            A user created Colormap object. Default is None.
        norm: Normalize, optional
            A user defined Normalize object. Default is None.
            Can be used to control 
        scatter: bool, optional
            Whether or not to use scatter as opposed to imshow.
        """
        self.norm = None
        if standard is not None:
            self.cmap = colormaps[standard]
        elif custom is not None:
            self.cmap = ListedColormap(custom, name='custom', N=None)
            self.norm = Normalize(vmin=0, vmax=len(custom)-1)
        else:
            self.cmap = None

    def plot(self, data):
        """
        Plots data using imshow() from Matplotlib. 

        Args
        ----
        data: array-like
            The data to plot. For instance, an N x M matrix representing the 
            game world.

        Returns
        -------
        None
        """

        plt.cla()
        plt.imshow(data, cmap=self.cmap, norm=self.norm)

    def scatter(self, x, y, xlim, ylim, c=None, redraw=True, s=rcParams['lines.markersize'] ** 2):
        """
        Plots data using scatter() from Matplotlib. 

        Args
         ----
        x: array-like
            x coordinates.
        y: array-like
            y coordinates.
        xlim: tuple
            Min and max value to plot in the x direction, e.g. (0, dim)
        ylim: tuple
            Min and max value to plot in the y direction, e.g. (0, dim)
        c: array-like, or int
            Values that correspond to the (x,y) coordinates. 
            Used for coloring. 

        """
        if type(c) is not list:
            c = [c] * len(x)

        if redraw:
            plt.cla()
        plt.scatter(x, y, c=c, cmap=self.cmap, norm=self.norm, s=s)
        plt.xlim(xlim)
        plt.ylim(ylim)

    def quiver(self, x, y, u, v, xlim, ylim):
        """
        Plots data using quiver() from Matplotlib. 

        Args
         ----
        x: array-like
            x coordinates.
        y: array-like
            y coordinates.
        u: array-like
            Velocity in the x-direction. 
        v: array-like
            Velocity in the y-direction. 
        xlim: tuple
            Min and max value to plot in the x direction, e.g. (0, dim)
        ylim: tuple
            Min and max value to plot in the y direction, e.g. (0, dim)
        c: array-like
            Values that correspond to the (x, y) coordinates. 
            Used for coloring. 

        """
        plt.cla()
        plt.quiver(x, y, u, v, width=0.005, scale=30)
        plt.xlim(xlim)
        plt.ylim(ylim)

    def show_stats(self, stats):
        """
        Sets the title of the simulation plot.
        Can be used to show stats about the simulation, such as
        the number of the current generation.

        Args
        ----
        stats: str
            The stats that are to be displayed.
        
        Returns
        -------
        None
        """
        plt.gca().set_title(stats)
