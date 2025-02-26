import math

class Repeller:
        def __init__(self, Katracao, Kintensidade, outputLimit):
                self.Katracao = Katracao
                self.Kintensidade = Kintensidade
                self.outputLimit = outputLimit

        def SetRepeller(self, Katr, Kint, new_outputLimit):
                if Katr < 0:
                        Katr = 0
                if Kint < 0:
                        Kint = 0
                if new_outputLimit < 0:
                        new_outputLimit = 0
                elif new_outputLimit > 100:
                        new_outputLimit = 100
                
                self.Katracao = Katr
                self.Kintensidade = Kint
                self.outputLimit = new_outputLimit

        def Update(self, erro):
                output = self.Katracao * math.exp(erro * self.Kintensidade)
                
                if output > self.outputLimit:
                        output = self.outputLimit
                
                return output
