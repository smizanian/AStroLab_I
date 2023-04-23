import math
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from scipy import constants as c


def linearFunc(x,intercept,slope):
    y = intercept + slope * x
    return y

def velocity(w, lambda_nm):
    temp = (w*(10**(-12)))/(lambda_nm*(10**(-9)))
    return c.c*temp

def d_velocity(dw, lambda_nm):
    temp = (dw*(10**(-12)))/(lambda_nm*(10**(-9)))
    return c.c*temp

def calculate_velocity(v2, dv2, w, dw):
    for i in range(len(w)):
        v2.append(velocity(w[i], lambda_nm[i])**2)
        dv2.append(d_velocity(dw[i], lambda_nm[i])**2)
    return

def calculate_m_bar(m_bar_1, A):
    for i in range(len(A)):
        temp = A[i]*c.m_p
        temp = 1/temp
        m_bar_1.append(temp)
    return    

def fit(m_bar_1, v2, dv2):
    a_fit,cov=curve_fit(linearFunc,m_bar_1,v2,sigma=dv2,absolute_sigma=True)
    inter = a_fit[0]
    slope = a_fit[1]
    d_inter = np.sqrt(cov[0][0])
    d_slope = np.sqrt(cov[1][1])
    return slope, d_slope, inter, d_inter

def temperature(slope):
    return slope/(2*c.k)

def d_temperature(d_slope):
    return d_slope/(2*c.k)

def turbulence(inter):
    return inter**0.5

# Group 5 datasets
w = [4.42, 0.58, 1.71]
dw = [0.1, 0.1, 0.1]
lambda_nm = [1083, 378, 1565]
A = [4, 27, 56]
v2 = []
dv2 = []
m_bar_1 = []

spec_type = "NOT DEFINED"

calculate_velocity(v2, dv2, w, dw)
calculate_m_bar(m_bar_1, A)

slope, d_slope, inter, d_inter=fit(m_bar_1, v2, dv2)

print("Temperature Units are in Kelvin. The Turbulence Speed Unit is in m/s")
print("Part A")
print("Temperature=")
print(temperature(slope))
print("d Temperature=")
print(d_temperature(d_slope))
print("Spectral Type=")
print(spec_type)

w = [0.94, 3.56]
dw = [0.1, 0.1]
lambda_nm = [378, 1565]
A = [27, 56]
v2 = []
dv2 = []
m_bar_1 = []

calculate_velocity(v2, dv2, w, dw)
calculate_m_bar(m_bar_1, A)

slope, d_slope, inter, d_inter=fit(m_bar_1, v2, dv2)
print("Part B")
print("Temperature=")
print(temperature(slope))
print("Turbulence Speed=")
print(turbulence(inter))

