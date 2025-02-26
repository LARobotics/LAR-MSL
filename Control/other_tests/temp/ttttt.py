
import matplotlib.pyplot as plt
import numpy as np

decay_rate = 0.5

def converge_to_desired(current_value, target_value, damping_factor=5, iterations=200):
    history = [current_value]
    history2 = [current_value]
    for i in range(iterations):
        #current_value += (1-damping_factor) * (target_value - current_value)
        
            #     if xx < 1 and xx > 0:
            #         xx = 1
            #     if xx > -1 and xx < 0:
            #         xx = -1
            # else:
            #     xx = 0    
                
        if abs(target_value - current_value) != 0:
            if target_value > current_value:
                xx = abs(target_value - current_value)*100/((target_value - current_value)**2)
                print("c", xx, end = ' ')
            else:
                xx = -abs(target_value - current_value)*100/((target_value - current_value)**2)
                print("b", xx, end = ' ')
        else:
            print("a", xx, end=' ')
            xx = 0
        
        # if (target_value - current_value)**2 != 0:
        #     if xx < 1 and xx > 0:
        #         xx = 1
        #     if xx > -1 and xx < 0:
        #         xx = -1
        # else:
        #     xx = 0
        # if abs(xx) > 10:
        #     if xx > 0:
        #         xx = min(10, xx)
        #     else:
        #         xx = max(-10, xx)
        
        #yy = abs(target_value - current_value)
        #xx = 
        
        # damping_factor = (abs(target_value - current_value))/100
        
        current_value += xx * damping_factor#* np.exp(decay_rate * i)
        if target_value > 0:
            current_value = min(current_value, target_value)
        else:
            current_value = max(current_value, target_value)
        print(i, current_value, target_value, xx, damping_factor)
        
        history.append(current_value)
        history2.append(xx)
        if i >= 50:
            target_value = -180
        # damping_factor -= factor_decay_rate

    return history, history2

def plot_convergence(history, target_value):
    """
    Function to plot the convergence history.
    
    Parameters:
    - history: List of values at each iteration.
    - target_value: Target value.
    """
    plt.plot(history, marker='o', linestyle='-')
    plt.axhline(y=target_value, color='r', linestyle='--', label='Target Value')
    plt.xlabel('Iteration')
    plt.ylabel('Value')
    plt.title('Convergence towards Target Value')
    plt.legend()
    plt.grid(True)

# Example usage:
current_value = 0  # Initial value
target_value = 180  # Target value

history, history2 = converge_to_desired(current_value, target_value)
plot_convergence(history, target_value)
# plot_convergence(history2, target_value)
plt.show()