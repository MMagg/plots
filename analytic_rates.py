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
import sys

del_c = 1.686
rho_m = 1e-26*0.3086/2e30*(3.08567758e22)**3 # [M_sun/mpc^3]
sigma_8=0.816
print rho_m
V = 1000 # [Mpc^3]
skip = 70
n = 1000 # number of redshift steps


def rho(z):
    return rho_m/(1.+z)^3
    
def dn_dm(m, sigma, alpha, z):
    ny = del_c/sigma
    y = np.sqrt(2./np.pi)*rho(z)/m**2*(-alpha)*ny*np.exp(-ny**2/2)
    # See Lacey&Cole 1991 eq 2.11
    return y

def m_crit(z):
    return 1.00e6*((1+z)/10.0)**(-1.5)*(2.200)**(1.5)

z_array = np.linspace(0, 35, n)

data = np.loadtxt(os.path.join('..', 'Code', 'Data', 'pk_Planck13.dat.spline'), skiprows = 1)
m = data[skip:,0]
sigma = data[skip:,1]
alpha = data[skip:,3] # d ln \sigma / d ln m
pisn_rate = np.zeros(n)
for i in range(n-1):
    dn = dn_dm(m, sigma, alpha, z)
    dn_func=iterp1d(m, dn)
    #N_pi = simps()
    


plt.figure(figsize = (8,8))
plt.yscale('log')
plt.ylabel(r'PISN rate $[(yr*Mpc^3)^{-1}]$')
plt.xlabel(r'$z$')


dN = sum(n_pi[j_file, :, i])
        dz = z_pi[j_file, i+1]-z_pi[j_file, i]
        dt = t_pi[j_file, i]-t_pi[j_file, i+1]
        dr = r_pi[j_file, i+1]-r_pi[j_file, i]
        rate_z_pi[j_file, i] = dN/dt/V*(z_pi[j_file, i]+1)**2*r_pi[j_file, i]**2*dr/dz/(rad_to_arcmin**2)*10
    cum_rate = cumtrapz(rate_z_pi[j_file, :], x=z_pi[j_file, :-1])
raw_input("Press enter to continue")