# import numpy as np
# import matplotlib.pyplot as plt

# def plot_vector(ax, angle, magnitude, color='b'):
#     x = np.deg2rad(angle)
#     ax.quiver(0, 0, x, magnitude, angles='xy', scale_units='xy', scale=1, color=color, width=0.01, headwidth=0, headlength=0)

# def interpolate_vectors(angle1, magnitude1, angle2, magnitude2, func, num_intermediate):
#     angles = np.linspace(angle1, angle2, num_intermediate + 2)  # Exclude the endpoints
#     print(angles)
#     magnitudes = func(np.linspace(0, 1, num_intermediate + 2))# * (magnitude2 - magnitude1) + magnitude1
#     return angles, magnitudes

# angle1_deg = 91
# magnitude1 = 1
# angle2_deg = 270
# magnitude2 = 1

# def linear_interpolation(t):
#     print(type(t))
#     x = (2*abs(t-0.5))**2
#     temp = 0.75
#     x = -temp*np.sin(3.14*t)+temp
#     # x = -16*(t**2-t)**2+1
#     # x = t
#     # for i in range(len(t)):
#     #     if t[i] > 0.5:
#     #         x[i] = -4*(t[i]-1)**2+1
#     #     else:
#     #         x[i] = -4*(t[i])**2+1
            
#     print(x)
#     return x

# num_intermediate = 11
# intermediate_angles, intermediate_magnitudes = interpolate_vectors(angle1_deg, magnitude1, angle2_deg, magnitude2, linear_interpolation, num_intermediate)
# fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

# plot_vector(ax, angle1_deg, magnitude1, color='b')
# plot_vector(ax, angle2_deg, magnitude2, color='r')

# for angle, magnitude in zip(intermediate_angles, intermediate_magnitudes):
#     plot_vector(ax, angle, magnitude, color='g')

# ax.set_theta_zero_location('N')

# ax.set_ylim(0, 1.2)
# plt.show()


# import numpy as np
# import matplotlib.pyplot as plt

# def plot_vector(ax, angle, magnitude, color='b'):
#     x = np.deg2rad(angle)
#     ax.quiver(0, 0, x, magnitude, angles='xy', scale_units='xy', scale=1, color=color, width=0.01, headwidth=0, headlength=0)

# def interpolate_vectors(angle1, magnitude1, angle2, magnitude2, func, num_intermediate):
#     angles = np.linspace(angle1, angle2, num_intermediate + 2)  # Exclude the endpoints
#     print(angles)
#     magnitudes = func(np.linspace(0, 1, num_intermediate + 2))# * (magnitude2 - magnitude1) + magnitude1
#     return angles, magnitudes


# def linear_interpolation(t):
#     temp = 0.75
#     x = -temp*np.sin(3.14*t)+temp
#     return x

# def calculate_num_intermediate_points(angle1_deg, magnitude1, angle2_deg, magnitude2):
#     angle_diff = abs(angle2_deg - angle1_deg)
#     magnitude_diff = abs(magnitude2 - magnitude1)
#     num_intermediate = int(2 * (angle_diff + magnitude_diff))
#     return min(max(num_intermediate, 2), 20)  # Ensure at least 2 intermediate points

# angle1_deg = 91
# magnitude1 = 1

# fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
# ax.set_theta_zero_location('N')
# ax.set_ylim(0, 1.2)

# for i in range(5):  # Number of iterations
#     angle2_deg = 270 + i * 20  # Example: Increment angle2_deg
#     magnitude2 = 1  # Example: Set magnitude2
    
#     num_intermediate = calculate_num_intermediate_points(angle1_deg, magnitude1, angle2_deg, magnitude2)
#     print(num_intermediate)
#     intermediate_angles, intermediate_magnitudes = interpolate_vectors(angle1_deg, magnitude1, angle2_deg, magnitude2, linear_interpolation, num_intermediate)
    
#     plot_vector(ax, angle1_deg, magnitude1, color='b')
#     plot_vector(ax, angle2_deg, magnitude2, color='r')
    
#     for angle, magnitude in zip(intermediate_angles, intermediate_magnitudes):
#         plot_vector(ax, angle, magnitude, color='g')
    
#     angle1_deg = angle2_deg
#     magnitude1 = magnitude2

# plt.show()


# import matplotlib.pyplot as plt

# def converge_to_desired(current_value, target_value, damping_factor=0.001, iterations=100):
#     history = [current_value]
#     for i in range(iterations):
#         current_value += damping_factor * (target_value - current_value)
#         if i >= 50:
#             target_value = 8
#         history.append(current_value)
#     return history

# def plot_convergence(history, target_value):
#     """
#     Function to plot the convergence history.
    
#     Parameters:
#     - history: List of values at each iteration.
#     - target_value: Target value.
#     """
#     plt.plot(history, marker='o', linestyle='-')
#     plt.axhline(y=target_value, color='r', linestyle='--', label='Target Value')
#     plt.xlabel('Iteration')
#     plt.ylabel('Value')
#     plt.title('Convergence towards Target Value')
#     plt.legend()
#     plt.grid(True)
#     plt.show()

# # Example usage:
# current_value = 0  # Initial value
# target_value = 10  # Target value

# history = converge_to_desired(current_value, target_value)
# plot_convergence(history, target_value)


import numpy as np
import matplotlib.pyplot as plt

def polar_to_cartesian(rho, theta):
    x = rho * np.cos(theta)
    y = rho * np.sin(theta)
    return x, y

def cartesian_to_polar(x, y):
    rho = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return rho, theta

def dampening_transition_polar(polar1, polar2, alpha, DAMP):
    rho1, theta1 = polar1
    rho2, theta2 = polar2

    rho_interpolated = (rho1+rho2)//2 * (1/(DAMP*np.sin(3.14*alpha)+1))

    # if alpha <= 0.5:
    #     rho_interpolated = rho1 * (1/(DAMP*np.sin(3.14*alpha)+1))
    # else:
    #     rho_interpolated = rho2 * (1/(DAMP*np.sin(3.14*alpha)+1))
    
    theta_interpolated = theta1 + (theta2 - theta1) * alpha
    return rho_interpolated, theta_interpolated

def plot_transition(polar1, polar2, num_frames=100, DAMP = 8):
    rho1, theta1 = polar1
    rho2, theta2 = polar2
    print(np.rad2deg(theta1), np.rad2deg(theta2))
    
    
    if abs(np.rad2deg(theta1+(2*np.pi) - theta2)) < abs(np.rad2deg(theta1 - theta2)):
        theta1 = theta1 + (2*np.pi)
    elif abs(np.rad2deg(theta1-(2*np.pi) - theta2)) < abs(np.rad2deg(theta1 - theta2)):
        theta1 = theta1 - (2*np.pi)
    polar1 = rho1, theta1
    print(np.rad2deg(theta1), np.rad2deg(theta2))
    
    max_rho = max(rho1, rho2)
    fig, ax = plt.subplots()

    DAMP = max(min(np.sqrt(np.rad2deg(abs(theta1 - theta2))/5), 20), 0.1)
    num_frames = int(DAMP**2)+1
    
    print(num_frames, DAMP)
    
    polar_interpolated = polar1
    for i in range(num_frames):
        alpha = i / max((num_frames - 1), 1)
        polar_interpolated = dampening_transition_polar(polar1, polar2, alpha, DAMP)
        x, y = polar_to_cartesian(*polar_interpolated)
        ax.plot([0, x], [0, y], color='blue')
        ax.plot(x, y, marker='o', color='red')
        plt.xlim(-max_rho, max_rho)
        plt.ylim(-max_rho, max_rho)
        plt.title(f'Frame {i+1}/{num_frames}')
        #ax.clear()

    plt.pause(0.01)
    plt.show()

# Example usage

#polar1 = (0.5, np.deg2rad(0))  # rho, theta
#for i in [30, 80, 120, 180, -90, -70, -5]:
while 1:
    #polar2 = (1, np.deg2rad(i))  # rho, theta
    #polar3 = (1, np.deg2rad(-80))  # rho, theta
    polar1 = (np.random.randint(20, 100), np.deg2rad(int(np.random.randint(-180, 180))))
    polar2 = (np.random.randint(20, 100), np.deg2rad(int(np.random.randint(-180, 180))))
    plot_transition(polar1, polar2)
    # while polar1 != polar2:
    #     polar1 = plot_transition(polar1, polar2)
    #     print(polar1, polar2)

# DAMP = max(min(int(np.rad2deg(abs(polar1[1] - polar2[1]))//10 - 1), 18), 2)
# polar1 = dampening_transition_polar(polar1, polar2, alpha, DAMP)

# plot_transition(polar1, polar2, num_frames=100, DAMP = 40)
# plot_transition(polar1, polar2, num_frames=100, DAMP = 80)

