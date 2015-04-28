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
n_mmin = 2
nlev = 256
mlev = 256
upper_limit = 1.4e4
V = 30 #Mpc^3


mbh_arr = np.zeros(nlev)
mbh_arr.fill(upper_limit)

print 'reading data'
files = glob.glob(os.path.join('output_sn', 'z_MBH_*'))
i_file = 0
n_file = len(files)

z = np.zeros((n_file, nlev))
mbh = np.zeros((n_file, nlev))
mbh_std = np.zeros((n_file, nlev))

for f in files:
    print os.path.basename(f)
    data = np.loadtxt(f)
    z[i_file, :] = data[:, 0]
    mbh[i_file, :] = data[:, 1]
    mbh_std[i_file, :] = data[:, 2]
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', files[i_file])
    i_file = i_file + 1


print 'plotting'
# plt.plot(False, False, color='white', label=(r'For $M_{max}=$'+str(float(paras[2]))+r'$M_{\odot}$'))
for j_file in range(n_file):
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', os.path.basename(files[j_file]))
    plt.plot(z[j_file, :], mbh[j_file, :], label=(r'$\eta=$'+str(float(paras[3]))+r'$M_{max}=$'+str(float(paras[2]))+r'$M_{\odot}$'))
    # '\n'+r'$M_{max}=$'+paras[2]+r'$M_{\odot}$'+
plt.plot(z[0, :], mbh_arr, label=('UXBR Limit'), color='grey', linestyle='-')
plt.fill_between(z[0, :], mbh_arr, 1.0e5, facecolor='grey')
#plt.plot(z[0, :], tau_arr-sig_tau, label=(r'$1\sigma$ error'), color='black', linestyle='-.')
#plt.plot(z[0, :], tau_arr+sig_tau, color='black', linestyle='-.')


plt.ylabel(r'Accreted Mass  $M[M_{\odot}]$', size=16)
plt.xlabel(r'redshift $z$', size = 16)
plt.xscale('linear')
plt.yscale('log')
plt.xlim(min(z[0, :]), 35)
plt.ylim(1, 1.0e5)
plt.legend(bbox_to_anchor=(1.5, 1.0))
plt.grid(b=True, which='both', color='0.65',linestyle='-')
plt.savefig('mbh.eps', bbox_inches='tight')
plt.savefig('mbh.jpg', bbox_inches='tight')
#plt.show()
plt.clf()

