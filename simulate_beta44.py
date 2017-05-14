import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

a = 4
b = 4
actual_answer = 25.4545

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
final_estimate = [[-70.608971423233584, 30.147532253779111, 30.735028955734631],
 [30.019007939805682, 37.930674422654128, 38.395068735115643],
 [27.942929279824007, 35.498742298656225, 36.816762638649294],
 [26.081263632801242, 31.854916592174721, 32.89077537344253],
 [23.693600304610406, 27.808353777941335, 28.616342410874495],
 [20.754312890176035, 23.700597725139641, 24.287323729235645],
 [17.768760702781705, 19.83039414266478, 20.231568075120034],
 [14.983213470593174, 16.407483937274943, 16.676585528376584],
 [12.523254470581673, 13.507285627208217, 13.687913821339148],
 [10.43189238587609, 11.116257797364835, 11.23882401035149]]

final_estimate = [[-105.14954510101134,
  18.69201764989155,
  38.184899267289545,
  41.256018333557876,
  41.182848555671725],
 [29.801594724758797,
  38.602458011445663,
  37.713311239435143,
  38.74974220373133,
  37.816296711002217],
 [35.783690818780187,
  38.489250923386408,
  35.717449158052155,
  36.086970854854492,
  35.224308770411561],
 [32.672411373185142,
  34.761818690024718,
  32.627643584664483,
  32.492079344213209,
  31.760053449942589],
 [28.838220735306159,
  30.217818903884332,
  28.629399528625761,
  28.351795617938816,
  27.76650036655812],
 [24.611234073187955,
  25.53704293327376,
  24.39571112347992,
  24.134119272462037,
  23.695665869104449],
 [20.558851482325167,
  21.154448280979544,
  20.352096804551412,
  20.154340573615411,
  19.842950707172182],
 [16.947968455932156,
  17.327191061426362,
  16.778175389721685,
  16.639571848240376,
  16.42467519456298],
 [13.89334912923052,
  14.137445894215864,
  13.764905100660952,
  13.669924900587716,
  13.523229161475577],
 [11.388286438379403,
  11.549487655387292,
  11.295153068782749,
  11.229917335585275,
  11.129416542935711]]

# estimating
final_estimate = [];
sigma = 0.1
for sigma in np.linspace(0.1, 1, 10):
	estimate = []
	for n1, n1 in [(50, 50), (300, 200), (500, 500), (800, 700), (1200, 800)]:
		n = n1 + n2
		estimate_2 =   (-n2*1.0/(n*n1*(n1-1)))* np.sum(cross(samples[0:n1],sigma))/N 
		estimate_3 =   (-n1*1.0/(n*n2*(n2-1)))* np.sum(cross(samples[n1:n],sigma))/N  

		estimate_1 = -2*individual(samples,sigma,n1,n2)

		estimate.append(estimate_1 + estimate_2 + estimate_3)

	final_estimate.append(estimate)

# calculate error
# error = final_estimate - actual_answer

# plotting
for i in range(10):
	plt.plot([100, 500, 1000, 1500, 2000], final_estimate[i], label='$\sigma = {value}$'.format(value=round((i+1)*0.1, 2)))

plt.plot([100, 500, 1000, 1500, 2000], [actual_answer]*5, linestyle='--', color='red', label='Actual value')
plt.legend(loc = 'best')
plt.title(r'Estimator for $\beta(4, 4)$ with different values of $\sigma$ and $n$')
plt.ylabel('Estimate')
plt.xlabel('No. of data points, $n$')
plt.show()
