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
n = 1 # number of galaxies to be sampled at the same time

if len(sys.argv) > 2:
    print 'error: only one argument excepted'
    print 'further arguments are ignored'
    print 'use -output or -nooutput'
    os.system("pause")


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
    # See Lacey&Cole 1991 eq 2.11
    return y

data = np.loadtxt(os.path.join('..', 'Code', 'Data', 'pk_Planck13.dat.spline'), skiprows = 1)
m = data[skip:,0]
sigma = data[skip:,1]
alpha = data[skip:,3] # d ln \sigma / d ln m
dn = dn_dm(m, sigma, alpha)
M_max = simps(dn*m, m)*V
print sum((dn[:-1]+dn[1:])/2*(m[1:]-m[:-1])*m[1:])*V
print V*trapz(dn*m, m)
print simps(dn*m, m)*V
print rho_m*V
raw_input("Press enter to continue")

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
gal_list = []
gal_list_low = []

while M_sum <= M_max:
    m_curr = sample(X_of_Xi, n)
    M_sum = M_sum +sum(m_curr)
    print M_sum/M_max*100., '%'
    for m1 in m_curr:
        if m1 > 1e9: # and m1<1e10  :
            gal_list.append(m1)
        #if m1 > 1e6 and m1<1e9 and np.random.random(1) < 0.05 :
        #gal_list_low.append(m1)
gal_list = np.array(gal_list)
plt.figure(figsize = (8,8))
plt.hist(gal_list, log = True, bins=np.logspace(9, 15, 60))
plt.xscale('log')
plt.ylabel('Number of clusters')
plt.xlabel(r'$M[M_{\odot}]$')

if M_sum/M_max*100.<102. and sys.argv[1] == '-output':
    print 'writing output to files'
    print 'Mass in high M halos:', sum(gal_list)
    print 'Number of high M halos:', len(gal_list)
    print 'Mass in low M halos:', sum(gal_list_low)/0.05
    gal_list = np.hstack([len(gal_list), gal_list])
    np.savetxt(os.path.join('..', 'work', 'Data', 'galaxy_list.dat'), gal_list)
    gal_list_low = np.hstack([len(gal_list_low), gal_list_low])
    np.savetxt(os.path.join('..', 'work', 'Data', 'galaxy_list_low.dat'), gal_list_low)
    plt.savefig('../plots/galaxy_distr.jpg')
elif M_sum/M_max*100.>=102. and sys.argv[1] == '-output':
    print 'ERROR: SAMPLING ENDED BY LARGE GALAXY'
    print 'NO OUTPUT FILES WRITTEN'
elif sys.argv[1] == '-nooutput':
    print 'output deactivated'
    print 'Mass in high M halos:', sum(gal_list)
    print 'Number of high M halos:', len(gal_list)
    print 'Mass in low M halos:', sum(gal_list_low)/0.05
else:
    print 'invalid argument'
    print 'use -output or -nooutput'
plt.show()    

"""
plt.plot(m, dn, '.')
plt.xscale('log')
plt.yscale('log')"""