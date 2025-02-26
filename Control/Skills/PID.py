
class PID:
        def __init__(self, kP:float, kI:float, kD:float, dt:float, outputLimit:int):
                self.kP = kP
                self.kI = kI
                self.kD = kD
                self.dt = dt
                self.outputLimit = outputLimit
                self.lastError = 0
                self.integral = 0

        def SetPid(self, new_kP, new_kI, new_kD, new_outputLimit):
                if new_kP < 0.0:
                        new_kP = 0.0
                if new_kI < 0.0:
                        new_kI = 0.0
                if new_kD < 0.0:
                        new_kD = 0.0
                if new_outputLimit < -100.0:
                        new_outputLimit = -100.0
                elif new_outputLimit > 100:
                        new_outputLimit = 100
                self.kP = new_kP
                self.kI = new_kI
                self.kD = new_kD
                self.outputLimit = new_outputLimit

        def Update(self, error, dt):
                #print("dt "+str(dt))
                # Proportional term
                pTerm = self.kP * error
                # Integral term
                self.integral += error * dt
                iTerm = self.kI * self.integral

                # Derivative term
                dTerm = self.kD * (error - self.lastError) / dt

                # Compute the output
                output = pTerm + iTerm + dTerm
                #print("output "+str(output))
                # Limit the output if necessary
                if output > self.outputLimit:
                        output = self.outputLimit
                elif output < -self.outputLimit:
                        output = -self.outputLimit

                if self.lastError * error < 0:
                        self.CleanIntegral()

                self.lastError = error

                return output

        def CleanIntegral(self):
                self.integral = 0