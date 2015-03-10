"""Author: M. Magg
Code for fast plotting Ba. project output data.
To be copied and modified for every application
"""
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import re

n_eta = 3
n_mmin = 3
tau_planck = 0.0907
sig_tau = 0.0054

print 'reading data'
f = os.path.join('..', 'imf_test', 'output_vanilla', 'para_mmin_eta_tau.dat')
data = np.loadtxt(f)
eta = data[:, 1]
mmin= data[:, 0]
tau = data[:, 2]
tau_std = data[:, 3]
eta_ax = np.zeros(n_eta+1)
mmin_ax = np.zeros(n_mmin+1)
tau_map = np.zeros((n_mmin, n_eta))
for i in range(n_mmin*n_eta):
    eta_ax[i%n_eta] = eta[i]
    mmin_ax[i/n_eta] = mmin[i]
    tau_map[i/n_eta, i%n_eta]  = (tau[i]-tau_planck)/sig_tau
print tau_map
mmin_ax[n_mmin] = 2*mmin_ax[n_mmin-1]-mmin_ax[n_mmin-2]
eta_ax[n_eta] = 2*eta_ax[n_eta-1]-eta_ax[n_eta-2]

print 'plotting'


plt.pcolormesh(eta_ax, mmin_ax, tau_map)

# plt.xlim(0.002, 0.03)
plt.ylabel(r'$M_{min}[M_{\odot}]$', size=20)
plt.xlabel(r'$\eta$')
plt.xscale('linear')
cbar = plt.colorbar()
plt.title(r'Final $\tau$')
plt.savefig('../plots/reproduced/tau_2.jpg', bbox_inches='tight')
plt.show()
plt.clf()

