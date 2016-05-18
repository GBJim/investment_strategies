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


	def normalize(self,weighted_desnity):

		minimum = np.min(weighted_desnity)
		if minimum <= 0:
			weighted_desnity += (1-minimum)

		return weighted_desnity



	def get_K(self, vector_k, goal, money ):
		k_range = goal - money
		weighted_desnity = np.dot(self.weight.T, vector_k[:, :k_range])
		weighted_desnity = self.normalize(weighted_desnity)
		#print(weighted_desnity)
		#print(k_range)
		probability_desnity = weighted_desnity / np.sum(weighted_desnity)
		#print(probability_desnity )
		#print(k_range)
		choice = np.random.choice(k_range,1, p=probability_desnity)[0]


		return choice+1
		

	def get_vector_k(self, goal):
		degree = self.degree
		vector_k = np.ones((degree+1, goal),dtype=int)

		for i in range(1, degree+1):
			vector_k[i,:] = np.arange(0, goal, dtype=int)
			vector_k[i,:] *=  vector_k[i-1,:] 
		#weighted_desnity = np.dot(self.weight.T, weighted_desnity)

		return vector_k

	def get_average_steps(self,goal=100, repetitions=100000):
		total_steps = 0
		for i in range(repetitions):
			total_steps += self.start_investment(goal)["total_steps"]
		return total_steps / repetitions


	def start_investment(self, goal=100):
		history = []
		steps = 0
		money = 0
		
		vector_k = self.get_vector_k(goal-money)
		#weighted_desnity = self.get_weighted_density(goal)

		#print(weighted_desnity)


		while(money < goal):

			k = self.get_K(vector_k, goal, money)
			reward = invest(k)
			steps += 1 
			money += reward
			history.append({"money":money, "reward":reward, "k":k, "steps":steps})

		return {"total_steps": steps, "history": history}


			



s = Strategy(degree=1)


goal = 1000
repetitions = 10**5


# F(x) = a + bx




a = 1
b = 1
s.weight[0] = a
s.weight[1] = b

print("\nRisky Strategy Average Steps:")


print(s.get_average_steps(goal, repetitions))

a = 1
b = 0
s.weight[0] = a
s.weight[1] = b
#print(s.get_weighted_density(10))
print("\nUniform Strategy Average Steps:")
print(s.get_average_steps(goal, repetitions))

a = 0
b = -1
s.weight[0] = a
s.weight[1] = b
#print(s.get_weighted_density(10))
print("\nSafe Strategy Average Steps:")

print(s.get_average_steps(goal, repetitions))




