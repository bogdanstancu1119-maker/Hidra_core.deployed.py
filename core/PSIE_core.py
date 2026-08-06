# inima - 95 stabil - 0 credite
import random, math
class PSIE_Core:
    def __init__(self):
        self.variatii=[{"id":i,"valoare":0.000001+random.random()*99.9999999} for i in range(95)]
    def calculeaza_J(self):
        m=sum(v["valoare"] for v in self.variatii)/95
        return math.sqrt(sum((v["valoare"]-m)**2 for v in self.variatii)/95)