import math
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

def linearFunc(x,intercept,slope):
    y = intercept + slope * x
    return y

# Group 5 datasets
m_v = [20.49, 20.28, 20.92, 22.15, 21.67, 20.67, 20.74, 21.15, 20.12, 21.25, 20.07, 20.6, 21.06, 20.09, 20.25, 21.29]
P = [24.69, 28.23, 19.07, 9.09, 12.13, 25.31, 21.37, 16.65, 30.99, 15.66, 31.99, 23.21, 17.53, 31.56, 28.64, 15.26]
d_m_v = [0.17, 0.18, 0.14, 0.11, 0.12, 0.17, 0.15, 0.14, 0.19, 0.13, 0.19, 0.16, 0.14, 0.2, 0.19, 0.13]
M_v = []
log_P = []

d = 2400000*0.306601

for i in range(len(m_v)):
    print(m_v[i])
    M_v.append(m_v[i]+5-5*math.log(d,10))
    log_P.append(math.log(P[i], 10))
    print(M_v[i])


a_fit,cov=curve_fit(linearFunc,log_P,M_v,sigma=d_m_v,absolute_sigma=True)

inter = a_fit[0]
slope = a_fit[1]
d_inter = np.sqrt(cov[0][0])
d_slope = np.sqrt(cov[1][1])

yfit = []
for i in range(len(log_P)):
    yfit.append(inter+slope*log_P[i])

plt.plot(log_P, yfit)
plt.xlabel("log(P[days])")
plt.ylabel("M_v")
plt.errorbar(log_P, M_v, yerr = d_m_v,fmt='o',ecolor = 'red',color='yellow')
plt.gca().invert_yaxis()
plt.show()

print("B:")
print(inter)
print("a:")
print(slope)
print("Vars:")
print(d_inter)
print(d_slope)

m_v = [25, 25.3, 25.1, 24.6, 24.4, 25.1, 25.3, 24.6, 25.4, 24.9]
P = [43.3, 40.6, 34.1, 31.1, 41.4, 42.7, 33.8, 43.6, 41.3, 33.3]
V = [575, 607, 478, 371, 406, 556, 516, 460, 649, 429]
d_V = [20, 6, 4,19, 14, 7, 4, 10, 13, 9]
M_v = []
r = []

for i in range(len(m_v)):
    print("M_v")
    M_v.append(inter+slope*math.log(P[i],10))
    print(M_v[i])
    print("r(Mpc)")
    r.append((10**((m_v[i]-M_v[i]+5)/5))/1000000)
    print(r[i])

a_fit,cov=curve_fit(linearFunc,r,V,sigma=d_V,absolute_sigma=True)

slope = a_fit[1]
d_slope = np.sqrt(cov[1][1])

yfit = []
for i in range(len(r)):
    yfit.append(slope*r[i])

plt.plot(r, yfit)
plt.xlabel("r(Mpc)")
plt.ylabel("V(km/s)")
plt.errorbar(r, V, yerr = d_V,fmt='o',ecolor = 'red',color='yellow')
plt.show()

print("Hubble Constant:")
print(slope)
print("Vars:")
print(d_slope)
