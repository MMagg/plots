"""Author: M. Magg
Code for fast plotting Ba. project output data.
To be copied and modified for every application
"""
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import re

n_mmax = 3
n_mmin = 3
nlev = 256
mlev = 256
tau_planck = 0.0961
sig_tau = 0.0054

tau_arr = np.zeros(nlev)
tau_arr.fill(tau_planck)

print 'reading data'
files = glob.glob(os.path.join('..', 'imf_test', 'output_mmax', 'z_tauIII*'))
files.sort()
i_file = 0
n_file = len(files)

z = np.zeros((n_file, nlev))
tau = np.zeros((n_file, nlev))
tau_std = np.zeros((n_file, nlev))

for f in files:
    print os.path.basename(f)
    data = np.loadtxt(f)
    z[i_file, :] = data[:, 0]
    tau[i_file, :] = data[:, 1]
    tau_std[i_file, :] = data[:, 2]
    i_file = i_file + 1


print 'plotting'
for j_file in [0, 1, 2]:
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', files[j_file])
    plt.plot(z[j_file, :], tau[j_file, :], label=(r'$M_{max}=$'+paras[2]+r'$[M_{\odot}]$'))
    # '\n'+r'$M_{max}=$'+paras[2]+r'$M_{\odot}$'+
plt.plot(z[0, :], tau_arr, label=('Planck 2014'), color='black', linestyle='-')
plt.plot(z[0, :], tau_arr-sig_tau, label=(r'$1\sigma$ error'), color='black', linestyle='-.')
plt.plot(z[0, :], tau_arr+sig_tau, color='black', linestyle='-.')


plt.ylabel(r'Final $\tau$', size=20)
plt.xlabel(r'$z$')
plt.xscale('linear')
plt.xlim(0, 35)
# plt.yscale('log')
plt.legend(bbox_to_anchor=(1.0, 0.5))
plt.title(r'Final $\tau$')
plt.grid(b=True, which='both', color='0.65',linestyle='-')
plt.savefig('../plots/reproduced/tau_mmax.jpg', bbox_inches='tight')
plt.show()
plt.clf()

