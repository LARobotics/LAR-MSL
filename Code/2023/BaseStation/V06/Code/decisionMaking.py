"""_This code is the decision making part of the code, so it will handle the risk and reward systems of the robots._
"""

import consts
import numpy as np
import pathFinding
import guiElements

def calculateGraph(Robots, BallHandler, show = 0):
	"""The calculate Graph function creates a graph or a map of all the possible passes and goals, and it also calculates their precentage of success

	Args:
		Robots (list): Its the list of all the Robots
		BallHandler (int): The ID of the robot that has the ball
		show (int, optional): It's a simple flag to activate the drawing of the lines or not. Defaults to 0.

	Returns:
		graphType: it returns the graph with their specific probabilities in distance mode
	"""
	graph = {"1":[],"2":[],"3":[],"4":[],"5":[],}
	for robot in Robots:
		for r in Robots:
			if r.robotID == robot.robotID:
				continue
			prob = getSucessProbability(consts.KICK, [robot.position, r.position])
			guiElements.drawLine(robot.position, r.position, prob)
			prob = round(-np.log(prob), 2)
			if prob >= 100:	prob = 100		#NEED TO BE VERIFIED OR CORRECTED
			if prob <= 0: prob = 0		#NEED TO BE VERIFIED OR CORRECTED
			graph[str(robot.robotID)].append((str(r.robotID), prob))
		prob = getSucessProbability("GOAL", [robot.position, (11, 0)])
		guiElements.drawLine(robot.position, (11, 0), prob)
		prob = round(-np.log(prob), 2)
		if prob >= 100: prob = 100		#NEED TO BE VERIFIED OR CORRECTED
		if prob <= 0: prob = 0		#NEED TO BE VERIFIED OR CORRECTED
		graph[str(robot.robotID)].append((str(0), prob))
	playersMap = pathFinding.Graph(graph)
	return playersMap

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
	"""getSuccessProbability returns the probability of the action that is testing based on their probability calculations function

	Args:
		action (int): Its the action that we want to get the probability of (Ex. KICK, GOAL, ...)
		args (list): Its their given arguments to pass onto their probability calculation function

	Returns:
		float: The probability of success of a determined action
	"""
	if action == consts.KICK: # args = [Robots, BallHandler-1, friend-1]
		return proabilityOfPass(np.sqrt(np.power((args[0][0] - args[1][0]), 2)+ np.power((args[0][1]- args[1][1]), 2)))
	if action == "GOAL":
		return probabilityOfGoal(np.sqrt(np.power((args[0][0] - args[1][0]), 2)+ np.power((args[0][1]- args[1][1]), 2)))
		
def proabilityOfPass(distance):
	"""This function returns the probability of success of a pass based on its distance\n
	For now its based on the bell curve calculated with the ideal pass distance and deviation

	Args:
		distance (float): Distance of pass in meters

	Returns:
		: probabilityOfSucess
	"""
	bestDistanceToPass = 2
	bestDistanceToGoal = 4
	deviation = 4
	times = 10
	# print(distance)
	return round(times*(1/(deviation*np.sqrt(2*3.14)))*np.exp(-(distance-bestDistanceToPass)*(distance-bestDistanceToPass)/(2*deviation*deviation)), 2)

def probabilityOfGoal(distance):
	"""This function returns the probability of success of a goal based on its distance\n
	For now its based on the bell curve calculated with the ideal goal distance and deviation

	Args:
		distance (float): Distance of goal in meters

	Returns:
		: probabilityOfSucess
	"""
	bestDistanceToPass = 2
	bestDistanceToGoal = 4
	deviation = 4
	times = 10
	# print("\n", distance)
	return round(times*(1/(deviation*np.sqrt(2*3.14)))*np.exp(-(distance-bestDistanceToGoal)*(distance-bestDistanceToGoal)/(2*deviation*deviation)), 2)
