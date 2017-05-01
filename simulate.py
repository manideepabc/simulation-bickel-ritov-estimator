import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

a = 4
b = 4

n1 = 1200
n2 = 800
sigma = 0.5

n = n1 + n2 
N = 1000

def h(x):
	k = 315.0/256
	y = k*(x**2-1)**4
	y[abs(x) > 1] = 0
	return y
	
def h1(x):
	k = 315.0/256
	y = 8*k*x*(x**2-1)**3
	y[abs(x) > 1] = 0
	return y

def h2(x):
	k = 315.0/256
	y = 48*k*(x**2)*(x**2-1)**2 + 8*k*(x**2-1)**3
	y[abs(x) > 1] = 0
	return y
	
def cross(samples,sigma):
	x = np.linspace(0,1,N)
	y = np.zeros(N)
	for i in range(len(samples)):
		for j in range(i,len(samples)):
			 y = y + h1((x-samples[i])/sigma)*h1((x-samples[j])/sigma)
	y = y/(sigma**4)		 
	return y
	
def individual(samples,sigma,n1,n2):
	y = 0
	n = n1 + n2 
	for i in range(n1):	
		y = y + np.sum((h2((samples[i]-samples[n1:n])/sigma)))
	y = y/(sigma**3)
	y = y/(n1*n2)
	return y			
	
samples = np.random.beta(a,b,size = n)
'''
sorted_samples = sorted(samples)
avg_dist = 0
for i in range(len(sorted_samples)-1):
	avg_dist = avg_dist + abs(sorted_samples[i+1] - sorted_samples[i])**2

sigma = np.sqrt(avg_dist/(n*4))
'''
'''
x = np.linspace(0,1,N)
plt.figure(1)
plt.hist(samples,bins='auto',normed = 1)
plt.hold(True)
plt.plot(x,beta.pdf(x,a,b))
plt.show()
'''

#kernel fiting
estimate_2 =   (-n2*1.0/(n*n1*(n1-1)))* np.sum(cross(samples[0:n1],sigma))/N 
estimate_3 =   (-n1*1.0/(n*n2*(n2-1)))* np.sum(cross(samples[n1:n],sigma))/N  

estimate_1 = -2*individual(samples,sigma,n1,n2)

print estimate_1 + estimate_2 + estimate_3
