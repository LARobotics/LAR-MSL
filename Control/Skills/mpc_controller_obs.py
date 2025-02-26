import casadi as ca
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.patches as patches

def convert_position_to_distance_direction(obstaclesPositions, robotPosition):

    numObstacles = obstaclesPositions.shape[1]
    distances = np.zeros(numObstacles)
    directions = np.zeros(numObstacles)

    media = 0  # Média do ruído
    desvio_padrao = 0.1  # Desvio padrão
    
    for i in range(numObstacles):
        ruido_dis = np.random.normal(media, desvio_padrao)
        ruido_dir = np.random.normal(media, desvio_padrao)

        dx = obstaclesPositions[0, i] - robotPosition[0]
        dy = obstaclesPositions[1, i] - robotPosition[1]
        
        distances[i] = np.sqrt(dx**2 + dy**2) + ruido_dis

        if distances[i] > 6:
            distances[i] = 50

        directions[i] = np.arctan2(dy, dx) + ruido_dir

    return distances, directions


class MPCControllerFatropOBS:
    def __init__(self, N=10, dt=0.025, numObstacles=20):
        
        self.N = N
        self.dt = dt * 4
        
        # Define os estados e controles
        self.x = ca.MX.sym('x')
        self.y = ca.MX.sym('y')
        self.states = ca.vertcat(self.x, self.y)
        self.n_states = self.states.size1()


        self.vx = ca.MX.sym('Vx')
        self.vy = ca.MX.sym('Vy')
        self.controls = ca.vertcat(self.vx, self.vy)
        self.n_controls = self.controls.size1()

        # Modelo cinemático
        ode = ca.vertcat(self.vx, self.vy)

        # Discretização do sistema
        sys = {"x": self.states, "u": self.controls, "ode": ode * self.dt}
        intg = ca.integrator('intg', 'rk', sys, {"simplify": True, "number_of_finite_elements": 4})
        
        self.F = ca.Function('F', [self.states, self.controls], [intg(x0=self.states, u=self.controls)["xf"]], ["x", "u"], ["xnext"])
        
        self.opti = ca.Opti()

        # Variáveis de otimização
        self.X = []
        self.U = []
        for k in range(N):
            self.X.append(self.opti.variable(self.n_states))
            self.U.append(self.opti.variable(self.n_controls))
        self.X.append(self.opti.variable(self.n_states))

        # Parâmetro de estado inicial
        self.X0 = self.opti.parameter(self.n_states)
        self.target = self.opti.parameter(self.n_states)

        self.num_obstacles = numObstacles
        self.obs_x = self.opti.parameter(self.num_obstacles)
        self.obs_y = self.opti.parameter(self.num_obstacles)
        # QUANDO TIVER VEL E DIR DOS ROBOS
        # self.obs_x = self.opti.parameter(self.N, self.num_obstacles)
        # self.obs_y = self.opti.parameter(self.N, self.num_obstacles)
        # self.radius = self.opti.parameter(self.N, self.num_obstacles)
        self.r0 = 1.5

        # Inicialização da função objetivo e restrições
        self.obj = 0
        Q = ca.diagcat(1, 1)
        R = ca.diagcat(1, 1)
        penalty_weight = 0.5
        barrier_weight = 50

        for k in range(N):

            if k==0:
                self.opti.subject_to(self.X[0]==self.X0)

            x_k = self.X[k]
            u_k = self.U[k]

            # Função objetivo
            self.obj += ca.mtimes([(x_k - self.target).T, Q, (x_k - self.target)])
            self.obj += ca.mtimes([u_k.T, R, u_k])
            
            # Multiple Shooting
            self.opti.subject_to(self.X[k + 1] == self.F(self.X[k], self.U[k]))

            # Velocity Constraints
            v_mag = u_k[0]**2 + u_k[1]**2
            self.obj += penalty_weight * ca.fmax(0, v_mag - 3.5**2)**2

            # Restrições de obstáculos

            # QUANDO TIVER VEL E DIR DOS ROBOS
            # for obs_idx in range(self.num_obstacles):
            #     distance_squared = (x_k[0] - self.obs_x[k, obs_idx])**2 + (x_k[1] - self.obs_y[k, obs_idx])**2
            #     self.obj += barrier_weight * ca.fmax(0, ((self.radius[k,obs_idx])**2 - distance_squared))**2

            for obs_idx in range(self.num_obstacles):
                distance_squared = (x_k[0] - self.obs_x[obs_idx])**2 + (x_k[1] - self.obs_y[obs_idx])**2
                self.obj += barrier_weight * ca.fmax(0, ((self.r0)**2 - distance_squared))**2

        self.opti.minimize(self.obj)

        # Configurações do solver
        options = {
            "expand": True,
            "fatrop": {"mu_init": 1,
                       "warm_start_init_point": True,
                       "tol": 0.1,
                       "max_iter": 50,
                       "print_level": 0,
                    },
            "error_on_fail": True,
            "print_time": 0,
            "structure_detection": "none",
            "debug": False,
            "jit": True,
            "jit_temp_suffix": False,  
            "jit_name": "mpc_obs_solver",
            "jit_options": {
                "flags": ["-O3", "-march=native", "-ffast-math", "-funroll-loops"]
            },
        }
        self.opti.solver("fatrop", options)

        # opts = {
        #     'ipopt.print_level': 0,
        #     'print_time': 0,
        #     'ipopt.tol': 1e-3,
        #     'ipopt.max_iter': 100,  
        #     'ipopt.tol': 1,
        #     'ipopt.max_iter': 50,  
        #     'ipopt.mu_strategy': 'adaptive', 
        #     'ipopt.warm_start_init_point': 'yes',
        #     'ipopt.linear_solver': 'mumps', 
        #     'jit': True,  
        #     "jit_options": {
        #         "flags": ["-O3", "-march=native", "-ffast-math", "-funroll-loops"]
        #     },
        # }
        # self.opti.solver('ipopt', opts)

        
        # Inicializar solução anterior
        self.prev_x_opt = None
        self.prev_u_opt = None

    def updateObstacles(self, distances, directions, current_state): #new_positions):
        # obs_x = np.zeros((self.N, self.num_obstacles))
        # obs_y = np.zeros((self.N, self.num_obstacles))
        # radius = np.zeros((self.N, self.num_obstacles))
        # for obs_idx in range(self.num_obstacles):
        #     x0, y0, vel, dir = new_positions[:, obs_idx]
        #     for k in range(self.N):
        #         obs_x[k, obs_idx] = x0 + vel * np.cos(dir) * k * self.dt
        #         obs_y[k, obs_idx] = y0 + vel * np.sin(dir) * k * self.dt
        #         radius[k, obs_idx] = self.r0 + ((k*vel)*0.02)  

        # self.opti.set_value(self.obs_x, obs_x)
        # self.opti.set_value(self.obs_y, obs_y)
        # self.opti.set_value(self.radius, radius)

        # QUANDO TIVER VEL E DIR DOS OBSTACULOS
        # obs_x = np.zeros((self.N, self.num_obstacles))
        # obs_y = np.zeros((self.N, self.num_obstacles))
        # radius = np.zeros((self.N, self.num_obstacles))

        # x_robot, y_robot = current_state

        # for obs_idx in range(self.num_obstacles):
        #     d0, theta0 = distances[obs_idx], directions[obs_idx]

        #     for k in range(self.N):
        #         d_k = d0  

        #         obs_x[k, obs_idx] = x_robot + d_k * np.cos(theta0)
        #         obs_y[k, obs_idx] = y_robot + d_k * np.sin(theta0)

        #         radius[k, obs_idx] = self.r0  

        # # Atualiza os parâmetros no otimizador
        # self.opti.set_value(self.obs_x, obs_x)
        # self.opti.set_value(self.obs_y, obs_y)
        # self.opti.set_value(self.radius, radius)

        obs_x = np.zeros((self.num_obstacles))
        obs_y = np.zeros((self.num_obstacles))

        x_robot, y_robot = current_state

        for obs_idx in range(self.num_obstacles):
            d0, theta0 = distances[obs_idx], directions[obs_idx] 

            obs_x[obs_idx] = x_robot + d0 * np.cos(theta0)
            obs_y[obs_idx] = y_robot + d0 * np.sin(theta0)  

        # Atualiza os parâmetros no otimizador
        self.opti.set_value(self.obs_x, obs_x)
        self.opti.set_value(self.obs_y, obs_y)


    def optimize(self, current_state, target_state, distances, directions): #MPC_OBS_data_queue_input, MPC_OBS_data_queue_output, event):

# while True:

#     print("MPC")

#     if not MPC_OBS_data_queue_input.empty():
        #st_T = time.perf_counter()
        #current_state, target_state, distances, directions = MPC_OBS_data_queue_input.get()


        obs_x = np.zeros((self.num_obstacles))
        obs_y = np.zeros((self.num_obstacles))

        x_robot, y_robot = current_state

        for obs_idx in range(self.num_obstacles):
            d0, theta0 = distances[obs_idx], directions[obs_idx] 

            obs_x[obs_idx] = x_robot + d0 * np.cos(theta0)
            obs_y[obs_idx] = y_robot + d0 * np.sin(theta0)  

        # Atualiza os parâmetros no otimizador
        self.opti.set_value(self.obs_x, obs_x)
        self.opti.set_value(self.obs_y, obs_y)
        
        x0_dm = ca.DM(current_state)
        target_dm = ca.DM(target_state)

        # Atualiza os parâmetros com o estado atual e o target
        self.opti.set_value(self.X0, x0_dm)
        self.opti.set_value(self.target, target_dm)

        # Warm start com soluções anteriores
        if self.prev_x_opt is not None and self.prev_u_opt is not None:
            for k in range(self.N):
                self.opti.set_initial(self.X[k], self.prev_x_opt[:, k])
                self.opti.set_initial(self.U[k], self.prev_u_opt[:, k])
            self.opti.set_initial(self.X[-1], self.prev_x_opt[:, -1])
        
        # Resolver problema de otimização
        st = time.perf_counter()
        self.sol = self.opti.solve()
        ft = time.perf_counter()

        
        # Armazena soluções para o warm start futuro
        self.x_opt = self.sol.value(ca.hcat(self.X)) 
        self.u_opt = self.sol.value(ca.hcat(self.U))

        # Atualizar os valores anteriores para a próxima otimização
        self.prev_x_opt = np.hstack([self.x_opt[:, 1:], self.x_opt[:, -1].reshape(-1, 1)])
        self.prev_u_opt = np.hstack([self.u_opt[:, 1:], self.u_opt[:, -1].reshape(-1, 1)])
        # self.prev_x_opt = x_opt
        # self.prev_u_opt = u_opt
        
        
        # Retorna os primeiros valores de otimização
        return self.sol.value(self.U[0]), self.u_opt, self.x_opt, (ft-st)

    #     MPC_OBS_data_queue_output.put((self.sol.value(self.U[0]), self.u_opt, self.x_opt, (ft-st)))
    
    #     ft_T = time.perf_counter()

    #     sleepTime = (self.dt - (ft_T-st_T))
    #     if sleepTime > 0:
    #         time.sleep(sleepTime)
        
    #     ft_T = time.perf_counter()
    #     #print((ft_T - st_T), "Hz :" , 1/(ft_T-st_T))
            
    # else:
    #     time.sleep(self.dt)

    # if event.is_set():  
    #     break

# Exemplo de uso
if __name__ == "__main__":
    current_state = np.array([0, 0])
    target_state = np.array([10,0])

    mpc = MPCControllerFatropOBS(N=20, dt=0.025, numObstacles=7)

    numObstacles = 80
    x_min, x_max = -7, 7
    y_min, y_max = -11, 11
    v_min_obs, v_max_obs = 0, 6

    x_positions = np.random.uniform(x_min, x_max, numObstacles)
    y_positions = np.random.uniform(y_min, y_max, numObstacles)
    obstaclesPositions = np.array([
        x_positions,             # X
        y_positions,             # Y
        np.zeros(numObstacles),  # V
        np.zeros(numObstacles)   # Theta
    ], dtype=np.float64)

    distances, directions = convert_position_to_distance_direction(obstaclesPositions, current_state)

    for _ in range(2):
        optimized_control, control_estimated, trajectory_estimated, processTime  = mpc.optimize(current_state, target_state, distances, directions)
        #print("Primeiros valores otimizados (Vx, Vy):", optimized_control)
        print("Tempo de Optimização:", processTime, "Process Frequency:", (1/processTime))
        time.sleep(1)
    
    fig, axs = plt.subplots()

    # obstaclesPositions = np.array([[5, 1, 5, 7, 7, 5, 2], # X
    #                             [0, 1, 2, 0, 4, -1, 0], # Y
    #                             [0, 0, 0, 0, 0, 0, 0], # V
    #                             [0, 0, 0, 0, 0, 0, 0]], # Theta
    #                             dtype=np.float64)
    circle_Obs = []
    for obs_idx in range(numObstacles):
        circle_Obs.append(Circle((obstaclesPositions[1, obs_idx], obstaclesPositions[0, obs_idx]), 0.28, edgecolor='red', facecolor='red'))
        axs.add_patch(circle_Obs[obs_idx])

    axs.plot(trajectory_estimated[1], trajectory_estimated[0], 'o-', label="Trajectory", color="b")
    axs.set_aspect('equal', adjustable='box')
    axs.grid()
    axs.legend()

    plt.show()