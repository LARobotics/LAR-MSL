"""_This code is the decision making part of the code, so it will handle the risk and reward systems of the robots._
"""

import consts
import numpy as np

NoLineOfPassRisk = 100

def getRisk(action, args):
	"""_This functions returns the risk of a specific action_

	Args:
		action (int): _This is the action that the function will evaluate_
		args (list): _It gives arguments that change from action to action_
	"""
	if action == consts.KICK: # args = [Robots, BallHandler-1, friend-1]
		return round(np.sqrt(np.power((args[0][args[1]].position[0] - args[0][args[2]].position[0]), 2)+ np.power((args[0][args[1]].position[1] - args[0][args[2]].position[1]), 2)),2,)
		
		#print(consts.KICK, args)
	return -1

def getReward(action, args):
	"""_This functions returns the reward of a specific action_

	Args:
		action (int): _This is the action that the function will evaluate_
		args (list): _It gives arguments that change from action to action_
	"""
	if action == consts.KICK: # args = [Robots, BallHandler-1, friend-1]
		return round(args[0][args[1]].position[0] - args[0][args[2]].position[0], 1)
		
		#print(consts.KICK, args)

		
		
def getSucessProbability(action,args):
	
	if action == consts.KICK: # args = [Robots, BallHandler-1, friend-1]
		return functionOfPass(np.sqrt(np.power((args[0][0] - args[1][0]), 2)+ np.power((args[0][1]- args[1][1]), 2)))
	if action == "GOAL":
		return functionOfGoal(np.sqrt(np.power((args[0][0] - args[1][0]), 2)+ np.power((args[0][1]- args[1][1]), 2)))
		
def functionOfPass(distance):
	bestDistanceToPass = 2
	bestDistanceToGoal = 4
	deviation = 4
	times = 10
	# print(distance)
	return round(times*(1/(deviation*np.sqrt(2*3.14)))*np.exp(-(distance-bestDistanceToPass)*(distance-bestDistanceToPass)/(2*deviation*deviation)), 2)

def functionOfGoal(distance):
	bestDistanceToPass = 2
	bestDistanceToGoal = 4
	deviation = 4
	times = 10
	# print("\n", distance)
	return round(times*(1/(deviation*np.sqrt(2*3.14)))*np.exp(-(distance-bestDistanceToGoal)*(distance-bestDistanceToGoal)/(2*deviation*deviation)), 2)
