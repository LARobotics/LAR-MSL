# import matplotlib.pyplot as plt

# class RobotController:
#     def __init__(self, max_acceleration, max_angular_velocity, attenuation_factor):
#         self.current_velocity = 0.0
#         self.current_direction = 0.0
#         self.max_acceleration = max_acceleration
#         self.max_angular_velocity = max_angular_velocity
#         self.attenuation_factor = attenuation_factor

#     def update_velocity_and_direction(self, desired_velocity, desired_direction, delta_time):
#         # Calculate the velocity difference and direction difference
#         velocity_diff = desired_velocity - self.current_velocity
#         direction_diff = desired_direction - self.current_direction
        
#         # Apply attenuation to smooth the change
#         velocity_change = self.attenuation_factor * velocity_diff
#         direction_change = self.attenuation_factor * direction_diff
        
#         # Limit the maximum change based on max_acceleration and max_angular_velocity
#         if abs(velocity_change) > self.max_acceleration * delta_time:
#             velocity_change = self.max_acceleration * delta_time * (velocity_change / abs(velocity_change))
        
#         if abs(direction_change) > self.max_angular_velocity * delta_time:
#             direction_change = self.max_angular_velocity * delta_time * (direction_change / abs(direction_change))
        
#         # Update the current velocity and direction
#         self.current_velocity += velocity_change
#         self.current_direction += direction_change

#         return self.current_velocity, self.current_direction

# # Initialize the robot controller with max acceleration, max angular velocity, and attenuation factor
# controller = RobotController(max_acceleration=5, max_angular_velocity=0.1, attenuation_factor=0.5)

# # Simulation parameters
# desired_velocity = 100.0
# desired_direction = 180.0
# delta_time = 0.1  # Time step in seconds
# steps = 100

# # Lists to store the results for plotting
# velocities = []
# directions = []

# # Run the simulation
# for step in range(steps):
#     current_velocity, current_direction = controller.update_velocity_and_direction(desired_velocity, desired_direction, delta_time)
#     velocities.append(current_velocity)
#     directions.append(current_direction)

# # Plot the results
# plt.figure(figsize=(14, 6))

# # Plot velocity
# plt.subplot(1, 2, 1)
# plt.plot(range(steps), velocities, label='Velocity')
# plt.axhline(y=desired_velocity, color='r', linestyle='--', label='Desired Velocity')
# plt.xlabel('Step')
# plt.ylabel('Velocity')
# plt.title('Velocity over Time')
# plt.legend()

# # Plot direction
# plt.subplot(1, 2, 2)
# plt.plot(range(steps), directions, label='Direction')
# plt.axhline(y=desired_direction, color='r', linestyle='--', label='Desired Direction')
# plt.xlabel('Step')
# plt.ylabel('Direction')
# plt.title('Direction over Time')
# plt.legend()

# plt.tight_layout()
# plt.show()
import numpy as np
import matplotlib.pyplot as plt

class RobotController:
    def __init__(self, max_acceleration, max_angular_velocity, attenuation_factor_velocity_plus, attenuation_factor_velocity_minus, attenuation_factor_angular):
        self.current_velocity = 0.0
        self.current_direction = 0.0
        self.max_acceleration = max_acceleration
        self.max_angular_velocity = max_angular_velocity
        self.attenuation_factor_velocity_plus = attenuation_factor_velocity_plus
        self.attenuation_factor_velocity_minus = attenuation_factor_velocity_minus
        self.attenuation_factor_angular = attenuation_factor_angular
        self.max_velocity = 100.0
        self.min_velocity = 0.0
        self.min_value_ang = 10

    def update_velocity_and_direction(self, desired_velocity, desired_direction, attenuation_factor_velocity_minus, attenuation_factor_velocity_plus, attenuation_factor_angular, min_value_ang):

        self.attenuation_factor_velocity_plus = attenuation_factor_velocity_plus
        self.attenuation_factor_velocity_minus = attenuation_factor_velocity_minus
        self.attenuation_factor_angular = attenuation_factor_angular
        self.min_value_ang = min_value_ang
        # Ensure desired_velocity is within bounds
        desired_velocity = np.clip(desired_velocity, self.min_velocity, self.max_velocity)
        direction_diff = desired_direction - self.current_direction
        factor = 1
        if direction_diff != 0:
            factor = abs((180-abs(direction_diff))/360)
        desired_velocity_2 = float(desired_velocity)*factor
        # print(desired_velocity_2)
        # desired_velocity_2 = np.clip(desired_velocity_2, 0, 100)
        velocity_diff = desired_velocity_2 - self.current_velocity
        
        
        # Calculate the velocity difference and direction difference
        
        if velocity_diff > 0:
            velocity_change = (1/velocity_diff) * self.attenuation_factor_velocity_plus
        elif velocity_diff < 0:
            velocity_change = (1/velocity_diff) * self.attenuation_factor_velocity_minus
        else:
            velocity_change = 0
        if abs(velocity_change) > abs(velocity_diff):
            velocity_change = velocity_diff

        #print(velocity_diff)


        if direction_diff != 0:
            direction_change = (1/direction_diff)*(100-self.current_velocity)*self.attenuation_factor_angular#(1/direction_diff) * (self.attenuation_factor_angular * ((100-self.current_velocity)/100))
        else:
            direction_change = 0
        if abs(direction_change) > abs(direction_diff):
            direction_change = direction_diff
            
        if self.current_velocity < self.min_value_ang:
            self.current_direction = desired_direction
        else:
            self.current_direction += direction_change
        
        self.current_velocity = np.clip(self.current_velocity + velocity_change, self.min_velocity, self.max_velocity)
        
        

        return self.current_velocity, self.current_direction, desired_velocity_2, direction_diff, factor, velocity_diff, desired_velocity

# Initialize the robot controller with max acceleration, max angular velocity, and attenuation factor
controller = RobotController(max_acceleration=1, max_angular_velocity=0.1, attenuation_factor_velocity_plus=13, attenuation_factor_velocity_minus=13, attenuation_factor_angular = 13)

# Simulation parameters
desired_velocity = 100.0
desired_direction = 1.0
delta_time = 4  # Time step in seconds
steps = 4000


#! Desacelaração com a diferença do angulo
#! Mudança de direção primeiro com base na velocidade linear
#! 

if __name__ == "__main__":
    # Lists to store the results for plotting
    velocities = []
    desired_velocities = []
    directions = []
    direction_diffs = []
    factores = []
    velocity_diffs = []
    desired_velocities_read = []
    desired_directions = []

    # Run the simulation
    for step in range(steps):
        # if step == 600:
        #     desired_velocity = 30
        #     desired_direction = 30
        # if step == 1100:
        #     desired_velocity = 00
        #     desired_direction = 00
            
        if step == 1500:
            desired_velocity = 100
            desired_direction = 180
        # if step == 2000:
        #     desired_velocity = 50
        #     desired_direction = 50
        if step == 3000:
            desired_velocity = 40
            desired_direction = 90
            
            
        current_velocity, current_direction, desired_velocity_2, direction_diff, factor, velocity_diff, desired_velocity = controller.update_velocity_and_direction(desired_velocity, desired_direction, delta_time)
        velocities.append(current_velocity)
        directions.append(current_direction)
        desired_velocities.append(desired_velocity_2)
        direction_diffs.append(direction_diff)
        factores.append(factor)
        velocity_diffs.append(velocity_diff)
        desired_velocities_read.append(desired_velocity)
        desired_directions.append(desired_direction)
        

    # Plot the results
    plt.figure(figsize=(14, 6))

    # Plot velocity
    plt.subplot(1, 2, 1)
    plt.plot(range(steps), velocities, label='Velocity')
    plt.plot(range(steps), desired_velocities, label='desired_velocities', linestyle='--')
    # plt.plot(range(steps), direction_diffs, label='direction diffs')
    # plt.plot(range(steps), desired_velocities_read, label='desired_velocities_read')
    # plt.plot(range(steps), velocity_diffs, label='velocity diffs')
    # plt.plot(range(steps), factores, label='direction diffs')
    # plt.axhline(y=desired_velocity, color='r', linestyle='--', label='Desired Velocity')
    plt.xlabel('Step')
    plt.ylabel('Velocity')
    plt.title('Velocity over Time')
    plt.legend()

    # Plot direction
    plt.subplot(1, 2, 2)
    plt.plot(range(steps), directions, label='factores')
    plt.plot(range(steps), desired_directions, label='factores')
    # plt.axhline(y=desired_direction, color='r', linestyle='--', label='Desired Direction')
    plt.xlabel('Step')
    plt.ylabel('Direction')
    plt.title('Direction over Time')
    plt.legend()

    plt.tight_layout()
    plt.show()
