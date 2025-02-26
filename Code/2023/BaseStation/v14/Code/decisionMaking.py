"""_This code is the decision making part of the code, so it will handle the risk and reward systems of the robots._
"""

import consts
import numpy as np
import pathFinding
import guiElements
from scipy.optimize import linear_sum_assignment

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
	graphprobs = {"1":[],"2":[],"3":[],"4":[],"5":[],} 
	for robot in range(len(Robots)):
		for r in range(robot+1, len(Robots)):
			if Robots[r].robotID == Robots[robot].robotID:
				continue
			prob = getSucessProbability(consts.KICK, [Robots[robot], Robots[r]])
			if consts.REPRESENT_LINES_OF_PASS:
				guiElements.drawLine(Robots[robot].position, Robots[r].position, prob)
			graphprobs[str(Robots[robot].robotID)].append((str(Robots[r].robotID), prob))
			graphprobs[str(Robots[r].robotID)].append((str(Robots[robot].robotID), prob))
			prob = max(min(100, round(-np.log(prob), 2)), 0)
			graph[str(Robots[robot].robotID)].append((str(Robots[r].robotID), prob))
			graph[str(Robots[r].robotID)].append((str(Robots[robot].robotID), prob))
		prob = getSucessProbability("GOAL", [Robots[robot], (11, 0)])
		if consts.REPRESENT_LINES_OF_PASS:
			guiElements.drawLine(Robots[robot].position, (11, 0), prob)
		graphprobs[str(Robots[robot].robotID)].append((str(0), prob))
		prob = max(min(100, round(-np.log(prob), 2)), 0)
		graph[str(Robots[robot].robotID)].append((str(0), prob))
	# playersMap = pathFinding.Graph(graph)
	# return playersMap
	return graph, graphprobs
		
def getSucessProbability(action,args):
	"""getSuccessProbability returns the probability of the action that is testing based on their probability calculations function

	Args:
		action (int): Its the action that we want to get the probability of (Ex. KICK, GOAL, ...)
		args (list): Its their given arguments to pass onto their probability calculation function

	Returns:
		float: The probability of success of a determined action
	"""
	if action == consts.KICK: # args = [Robots, BallHandler-1, friend-1]
		return proabilityOfPass(np.sqrt(np.power((args[0].position[0] - args[1].position[0]), 2)+ np.power((args[0].position[1]- args[1].position[1]), 2)), args[0].linesOfPassCutted[args[1].robotID], args[1].linesOfPassCutted[args[0].robotID])
	if action == "GOAL":
		return probabilityOfGoal(np.sqrt(np.power((args[0].position[0] - args[1][0]), 2)+ np.power((args[0].position[1]- args[1][1]), 2)), args[0].linesOfPassCutted[0])
		

def proabilityOfPass(distance, linesOfPassCutted1, linesOfPassCutted2):
	"""This function returns the probability of success of a pass based on its distance\n
	For now its based on the bell curve calculated with the ideal pass distance and deviation

	Args:
		distance (float): Distance of pass in meters
		linesOfPassCutted1 (list): Is the lines of pass cutted from A to B
		linesOfPassCutted2 (list): IS the lines of pass cutted from B to A
	Returns:
		: probabilityOfSucess
	"""

	bestDistanceToPass = consts.bestDistanceToPass
	bestDistanceToGoal = consts.bestDistanceToGoal
	deviation = consts.deviation
	times = consts.deviationPower
	
	probability = times*(1/(deviation*np.sqrt(2*3.14)))*np.exp(-(distance-bestDistanceToPass)*(distance-bestDistanceToPass)/(2*deviation*deviation))

	# NOTE: It is required to check both lines of pass, otherwise there would be a preference for the robot to lower ID
	# 		This way we can calculate one probability and use to pass from A to B and B to A

	if linesOfPassCutted1 != []:
		for lines in linesOfPassCutted1:
			probability *= (lines[2]/(consts.MARGIN2PASS*consts.MARGIN2CHECKPASS))
	if linesOfPassCutted2 != []:
		for lines in linesOfPassCutted2:
			probability *= (lines[2]/(consts.MARGIN2PASS*consts.MARGIN2CHECKPASS))
	return round(probability, 2)

def probabilityOfGoal(distance, linesOfPassCutted):
	"""This function returns the probability of success of a goal based on its distance\n
	For now its based on the bell curve calculated with the ideal goal distance and deviation

	Args:
		distance (float): Distance of goal in meters

	Returns:
		: probabilityOfSucess
	"""
	bestDistanceToPass = consts.bestDistanceToPass
	bestDistanceToGoal = consts.bestDistanceToGoal
	deviation = consts.deviation
	times = consts.deviationPower
	
	probability = times*(1/(deviation*np.sqrt(2*3.14)))*np.exp(-(distance-bestDistanceToPass)*(distance-bestDistanceToPass)/(2*deviation*deviation))

	# NOTE: This one also checks from A to the goal and the goal to A
	#? THIS IS COMMENTED TO DONT ACCOUNT FOR THE OPONENTS WHEN CALCULATING THE PROBABILITY OF GOAL
	if linesOfPassCutted != []:
		for lines in linesOfPassCutted:
			probability *= (lines[2]/(consts.MARGIN2PASS*consts.MARGIN2CHECKPASS))
   
		# probability *= (linesOfPassCutted[0][2]/(consts.MARGIN2PASS*consts.MARGIN2CHECKPASS))

	return round(probability, 2)

def hungarian(pointsA, pointsB):
    distances = np.zeros((len(pointsA), len(pointsB)))
    for i in range(len(pointsA)):
        for j in range(len(pointsB)):
            distances[i, j] = np.linalg.norm(pointsA[i] - pointsB[j])
    row, col = linear_sum_assignment(distances)
    return row, col, distances
