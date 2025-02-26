from collections import deque
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.style as mplstyle
import signal

mplstyle.use(['fast'])
matplotlib.use('TkAgg')

# def signal_handler(sig, frame):
#     plt.close()
#     exit(0)

# signal.signal(signal.SIGINT, signal_handler)
class RealTimePlot:
    def __init__(self, maxlen=50, xName = "Time", yName = "Variable Y", Scale = -1, angleMode = 0, pos = [-1, -1]):
        self.maxlen = maxlen
        self.data = deque(maxlen=maxlen)
        self.angleMode = angleMode
        if angleMode == 0:
            self.fig, self.ax = plt.subplots()
            self.line, = self.ax.plot([], [])
        else:
            self.ymin, self.ymax = 0, maxlen
            self.fig, self.ax = plt.subplots(subplot_kw={'projection': 'polar'})
            self.line, = self.ax.plot([], [], marker='o')
            self.ax.set_theta_direction(-1)  # Clockwise direction
            self.ax.set_theta_zero_location('N')  # Zero angle at North
            self.ax.set_ylim(self.ymin, self.ymax)
            self.ax.set_yticks(np.arange(self.ymin, self.ymax, self.ymax))  # Customize y-axis ticks

        if pos[0] != -1:
            self.fig.canvas.manager.window.overrideredirect(True)
            self.fig.canvas.manager.window.title(yName)
            temp = f"+{pos[0]}+{pos[1]}"
            self.fig.canvas.manager.window.geometry(temp)
            temp = f"{1920//5}x{1920//5}"
            self.fig.canvas.manager.window.geometry(temp)
            
        self.fig.canvas.manager.window.attributes('-topmost', 1)
        # #After placing figure window on top, allow other windows to be on top of it later
        self.fig.canvas.manager.window.attributes('-topmost', 0)
            
        self.yName = yName
        self.ax.set_xlabel(xName)
        self.ax.set_ylabel(yName)
        self.ax.set_title(yName)
        if Scale != -1 and not angleMode:
            self.ax.set_ylim(Scale[0], Scale[1])
        self.ax.grid(True)
        
        plt.show(block=False)
        
    def __str__(self):
        return str(self.data)
        
    def update_plot(self, new_value):
        
        if not self.angleMode:
            self.data.append(new_value)
            self.line.set_xdata(range(-len(self.data), 0))
            self.line.set_ydata(self.data)
            self.ax.relim()
            self.ax.autoscale_view()
        else:
            self.data.append(new_value)
            self.line.set_data(np.deg2rad(list(self.data)), range(len(self.data)))  # Update line data
        
        self.ax.set_title(f"{self.yName}: {self.data[-1]}")
        # self.ax.clear()
        
        # last_value = self.data[-1]
        # if not self.angleMode:
        #     self.ax.annotate(f'{last_value}', xy=(len(self.data)-1, last_value), xytext=(-5, 5), textcoords='offset points')
        # else:
        #     self.ax.annotate(f'{last_value}', xy=(np.deg2rad(last_value), len(self.data)-1), xytext=(-5, 5), textcoords='offset points')

        # #self.fig.canvas.draw()
    
    def show_plot(self):
        
        backend = plt.rcParams['backend']
        if backend in matplotlib.rcsetup.interactive_bk:
            figManager = matplotlib._pylab_helpers.Gcf.get_active()
            if figManager is not None:
                canvas = figManager.canvas
                if canvas.figure.stale:
                    canvas.draw()
                canvas.start_event_loop(0.001)
                return


def show_plot():
    try:
        plt.pause(0.001)
        return True
    except KeyboardInterrupt:
        return False

    
    # backend = plt.rcParams['backend']
    # if backend in matplotlib.rcsetup.interactive_bk:
    #     figManager = matplotlib._pylab_helpers.Gcf.get_active()
    #     if figManager is not None:
    #         canvas = figManager.canvas
    #         if canvas.figure.stale:
    #             canvas.draw()
    #         canvas.start_event_loop(0.001)
    #         return

if __name__ == "__main__":
    import numpy as np
    import time

    real_time_plot = RealTimePlot()

    while 1:
        new_value = np.random.random()
        real_time_plot.update_plot(new_value)
        real_time_plot.show_plot()
