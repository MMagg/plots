"""Program to sample values from a propability distribution
Author: M. Magg""" 

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumtrapz
from scipy.integrate import simps
from numpy import trapz
from scipy.interpolate import interp1d
import scipy
import os

del_c = 1.686
rho_m = 1e-26*0.3086/2e30*(3.08567758e22)**3 # [M_sun/mpc^3]
sigma_8=0.816
print rho_m
V = 1000 # [Mpc^3]
skip = 70
n = 1 # number of galaxies to be sampled at the same time

def sample_mass(dn, m, n=1): # Function to sample random values
    a = np.random.random(n)
    x = m
    cx = cumtrapz(dn, x=x, initial=0)
    cx = np.hstack([0, cx])
    X_of_Xi = interp1d(cx, m)
    return X_of_Xi(a)

def sample(X_of_Xi, n=1):
    a = np.random.random(n)
    return X_of_Xi(a)
    
def dn_dm(m, sigma, alpha):
    ny = del_c/sigma
    y = np.sqrt(2./np.pi)*rho_m/m**2*(-alpha)*ny*np.exp(-ny**2/2)
    return y

data = np.loadtxt(os.path.join('..', 'imf_test', 'Data', 'pk_Planck13.dat.spline'), skiprows = 1)
m = data[skip:,0]
sigma = data[skip:,1]
alpha = data[skip:,3]
dn = dn_dm(m, sigma, alpha)
M_max = simps(dn*m, m)*V
print sum((dn[:-1]+dn[1:])/2*(m[1:]-m[:-1])*m[1:])*V
print trapz(dn*m, m)*V
print simps(dn*m, m)*V
print rho_m*V

x = m[::-1]
dn = dn[::-1]
cx = cumtrapz(dn, x=x)
cx = np.hstack([0, cx])
cx = cx/cx[-1]
"""plt.plot(x, cx)
plt.xscale('log')
plt.yscale('log')
"""
X_of_Xi = interp1d(cx, x)

M_sum = 0
gal_list_8 = []
gal_list_9 = []
gal_list_10 = []
gal_list_11 = []

plt.show()
while M_sum <= M_max:
    m_curr = sample(X_of_Xi, n)
    M_sum = M_sum +sum(m_curr)
    print M_sum/M_max*100., '%'
    for m1 in m_curr:
        if m1 > 1e8 and m1<1e9  :
            gal_list_8.append(m1)
        if m1 > 1e9 and m1<1e10  :
            gal_list_9.append(m1)
        if m1 > 1e10 and m1<1e11  :
            gal_list_10.append(m1)
        if m1 > 1e11 and m1<1e12  :
            gal_list_11.append(m1)
gal_list_8 = np.array(gal_list_8)
gal_list_9 = np.array(gal_list_9)
gal_list_10 = np.array(gal_list_10)
gal_list_11 = np.array(gal_list_11)
plt.show()
if M_sum/M_max*100.<102.:
    print 'writing output to files'
    gal_list_8 = np.hstack([len(gal_list_8), gal_list_8])
    np.savetxt(os.path.join('..', 'work', 'Data', 'galaxy_list_8.dat'), gal_list_8)
    gal_list_9 = np.hstack([len(gal_list_9), gal_list_9])
    np.savetxt(os.path.join('..', 'work', 'Data', 'galaxy_list_9.dat'), gal_list_9)
    gal_list_10 = np.hstack([len(gal_list_10), gal_list_10])
    np.savetxt(os.path.join('..', 'work', 'Data', 'galaxy_list_10.dat'), gal_list_10)
    gal_list_11 = np.hstack([len(gal_list_11), gal_list_11])
    np.savetxt(os.path.join('..', 'work', 'Data', 'galaxy_list_11.dat'), gal_list_11)
else:
    print 'ERROR: SAMPLING ENDED BY LARGE GALAXY'
    print 'NO OUTPUT FILES WRITTEN'

"""
plt.plot(m, dn, '.')
plt.xscale('log')
plt.yscale('log')"""