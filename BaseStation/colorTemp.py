'''
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

x = np.arange(0, 10, 0.1)
y = x  

# Get all colormaps
gradients = [m for m in plt.cm.datad if not m.endswith("_r")]

# Display colormaps
fig, axes = plt.subplots(nrows=len(gradients) // 2, ncols=2, figsize=(10, 60),
                         subplot_kw={'xticks':[], 'yticks':[]})

for ax, gradient in zip(axes.flat, gradients):
    ax.imshow(y[np.newaxis, :], aspect='auto', cmap=plt.get_cmap(gradient))
    ax.set_title(gradient)

fig.tight_layout()
plt.show()
'''
import matplotlib.pyplot as plt 
import numpy as np

x = np.arange(0, 10, 0.1)
y = x

top_gradients = ['viridis', 'plasma', 'inferno', 'magma', 'cividis',
                 'Greys', 'Purples', 'Blues', 'Greens', 'Reds',
                 'YlOrBr', 'YlOrRd']#'Oranges', 'OrRd', 'PuRd', 'RdPu', 'BuPu',                 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',                 'PiYG', 'PRGn']

fig, axes = plt.subplots(nrows=12, ncols=1, figsize=(12, 18),
                         subplot_kw={'xticks': [], 'yticks': []})

for ax, gradient in zip(axes.flat, top_gradients):
    im = ax.imshow(y[np.newaxis, :], aspect='auto', cmap=plt.get_cmap(gradient))
    
    # Get center x,y coordinate
    xcenter = ax.get_xlim()[1]/2 
    ycenter = ax.get_ylim()[1]/2
    
    # Get the colormap name 
    # cmap_name = top_gradients[i]
    
    # Add text at center
    ax.text(xcenter, ycenter, "\n"+gradient, ha='center', va='center', fontsize=16)
    # Set the text with the colormap name at middle tick
    # cb.ax.text(mid_tick, 0.5, gradient, ha='center', va='center', fontsize=12)

    # ax.set_title(gradient)
    

fig.tight_layout()
plt.show()