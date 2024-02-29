import matplotlib
matplotlib.use('module://pygame_matplotlib.backend_pygame')
import matplotlib.pyplot as plt
import time
# fig, ax = plt.subplots()  # Create a figure containing a single axes.
# ax.plot([1, 2, 3, 4], [1, 4, 2, 3])  # Plot some data on the axes.

# for i in range(200):
# 	# plt.show()
import pygame
import pygame.display


fig, axes = plt.subplots(1, 1,)
axes = fig.gca()
axes.plot([1,2], [1,2], color='green', label='test')
fig.canvas.draw()

screen = pygame.display.set_mode((800, 600))

i = 0
show = True
while show:
	t = time.time()
	i += 0.01
	print(int((time.time()-t)*1000), end= " | ")
	# axes.draw_artist(axes.patch) # Draws the white around the 
	lines, = axes.plot([i, i+1, i+2, i+3], [i, i-1, i-2, i-3])  # Plot some data on the axes.
	axes.draw_artist(lines)
	print(int((time.time()-t)*1000), end= " | ")
	screen.blit(fig, (0, 0))
	print(int((time.time()-t)*1000), end= " | ")
	pygame.display.update()
	print(int((time.time()-t)*1000))
    