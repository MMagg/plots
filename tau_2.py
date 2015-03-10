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

print 'reading data'
f = os.path.join('..', 'imf_test', 'output_vanilla', 'para_mmin_eta_tau.dat')
data = np.loadtxt(f)
eta = data[:, 1]
mmin= data[:, 0]
tau = data[:, 2]
tau_std = data[:, 3]
eta_ax = np.zeros(n_eta)
mmin_ax = np.zeros(n_mmin)
tau_map = np.zeros((n_mmin, n_eta))
for i in range(n_mmin*n_eta):
    eta_ax[i%n_eta] = eta[i]
    mmin_ax[i/n_eta] = mmin[i]
    tau_map[i/n_eta, i%n_eta]  = tau[i]


print 'plotting'


plt.pcolor(eta_ax, mmin_ax, tau_map)

plt.ylabel(r'$M_{min}[M_{\odot}]$', size=20)
plt.xlabel(r'$\eta$')
plt.xscale('linear')
cbar = plt.colorbar()
plt.title(r'Final $\tau$')
plt.savefig('../plots/reproduced/tau.jpg', bbox_inches='tight')
plt.show()
plt.clf()

