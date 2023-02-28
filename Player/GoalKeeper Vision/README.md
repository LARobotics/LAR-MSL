![LAR](https://github.com/MSL-LAR-MinhoTeam/2TDP/blob/main/Images/git_msl_GK_vision.png)
# GoalKeeper Vision

## Ball Detection
This algorithm is able to detect the ball using computer vision, giving the system the coordinates of the ball in the camera.

## Ball Trajectory Prediction
The ball trajectory prediction is done using linear equations and the RGB-D camera (kinect).
The system take two consecutive frames, and if the ball is moving towards the goalkeeper, using the ball detection and the distance channel, is possible to obtain a linear equation that give us the ball trajectory.

## GoalKeeper Response
With the equation of ball trajectory, the system make the goalkeeper intercept the ball to defend the goal. In the ball trajectory equation, when y = 0, is where the goalkeeper needs to defend the ball, so with that position, the system verify if the ball is going to the goal or not, and if yes the goalkeeper will go to that position.
