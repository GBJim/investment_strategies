from random import randint
import numpy as np

invest = lambda k: k if randint(1,k) == 1 else 0

def get_exptection(k,times=10000000):
	earn = 0
	for i in range(times):
		earn += invest(k)


	return earn / times



class Strategy(object):

	def __init__(self, degree=1):
		self.degree = degree
		self.weight = np.ones(degree+1, dtype=float)
		self.weight[1:] = np.random.rand(degree)


	def get_K(self, weighted_desnity, goal, money ):
		k_range = goal - money


		probability_desnity = weighted_desnity[0:k_range] / np.sum(weighted_desnity[0:k_range])
		choice = np.random.choice(k_range,1, p=probability_desnity)[0]


		return choice+1
		

	def get_weighted_density(self, goal):
		degree = self.degree
		weighted_desnity = np.ones((degree+1, goal),dtype=int)

		for i in range(1, degree+1):
			weighted_desnity[i,:] = np.arange(1, goal+1, dtype=int)
			weighted_desnity[i,:] *=  weighted_desnity[i-1,:] 
		weighted_desnity = np.dot(self.weight.T, weighted_desnity)

		return weighted_desnity

	def get_average_steps(self,goal=100, repetitions=100000):
		total_steps = 0
		for i in range(repetitions):
			total_steps += self.start_investment(goal)["total_steps"]
		return total_steps / repetitions


	def start_investment(self, goal=100):
		history = []
		steps = 0
		money = 0
		

		weighted_desnity = self.get_weighted_density(goal)

		#print(weighted_desnity)


		while(money < goal):
			k = self.get_K(weighted_desnity, goal, money)
			reward = invest(k)
			steps += 1 
			money += reward
			history.append({"money":money, "reward":reward, "k":k, "steps":steps})

		return {"total_steps": steps, "history": history}


			



s = Strategy(degree=3)

#result = s.start_investment(100)
print(s.get_average_steps())
#print(result["history"])
#print(result["total_steps"])






