from random import randint
import numpy as np

invest = lambda k: np.random.choice([0,k],1,p=[1-(1/k),1/k])[0]

def get_exptection(k,times=100):
	earn = 0
	for i in range(times):
		earn += invest(k)


	return earn / times



class Strategy(object):

	def __init__(self, degree=None, parameters=None, customized_decision=None):
		
		if degree is None:
			self.degree = None
			if not customized_decision is None:
				self.decision_function = customized_decision
			else: 
				self.decision_function = self.get_K



		else:
			self.degree = degree
			self.weight = np.ones(degree+1, dtype=float)
			if parameters is None:
				self.weight = np.random.rand(degree+1)

			elif len(parameters) == degree + 1:
				self.weight = np.array(parameters)

			self.decision_function = self.get_K

			
	def normalize(self,weighted_desnity):

		minimum = np.min(weighted_desnity)
		if minimum <= 0:
			weighted_desnity += (1-minimum)

		return weighted_desnity



	def get_K(self, goal, money, vector_k ):
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
		if self.degree is None:
			return None

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


	def get_k_frequency(self, goal=100, repetitions=100):
		k_frequency = [0] * goal
		for i in range(repetitions):
			history = self.start_investment(goal)["history"]
			for record in history:
				k = record["k"] - 1
				k_frequency[k] += 1
		return k_frequency 


	def start_investment(self, goal=100, write_file_name = None):
		history = []
		steps = 0
		money = 0
		
		vector_k = self.get_vector_k(goal-money)

		



		while(money < goal):

			k = self.decision_function(goal, money, vector_k )
			reward = invest(k)
			steps += 1 
			money += reward
			history.append({"money":money, "reward":reward, "k":k, "steps":steps})


		if not write_file_name is None:
			self.history_to_file(history, write_file_name)

		return {"total_steps": steps, "history": history}



	def history_to_file(self, history, write_file_name):
		w = open(write_file_name, "w")
		w.write("steps, selected_k, reward, current_money\n")
		for record in history:
			w.write("{}, {}, {}, {}\n".format(record["steps"], record["k"], record["reward"], record["money"]))

		w.close()
		print("Output file {} has been writen.".format(write_file_name))

	def get_multiple_steps(self,goal, repetitions):
		steps = []
		for i in range(repetitions):
			result = self.start_investment(goal)
			steps.append(result["total_steps"])

		return steps





# Each strategy is represented by a polynomial probability density function
# A strategy object is intialized by two arguments, "degree" and "parameters"
# "degress" means the degree of polynomial
# The following is an example probability density function F(x) = a + bx when a=b=1
degree = 1
a = 1
b = 1
parameters= [a,b]
s = Strategy(degree, parameters)

if  __name__ == '__main__':

# We set goal as 10 for the following examples
	goal = 10

#Simulate an investment:
	result = s.start_investment(goal)

#Get the total steps form the investment result and historical records as well
	print(result["total_steps"])
	print(result["history"])

#You can also write the historical records into a file. CSV format is provided
	write_file_name = "my_investment_record.csv"
	s.start_investment(goal, write_file_name)


#Calculate the average steps for a given repetitions: 100
	print(s.get_average_steps(goal, 100))

