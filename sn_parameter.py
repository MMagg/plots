"""Author: M. Magg
Code for fast plotting Ba. project output data.
To be copied and modified for every application
"""
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import re

nlev = 256
mlev = 256
yr = (31557600)**(-1)


files = glob.glob(os.path.join('..', 'imf_test', 'output_vanilla', 'sn_rates', '*.dat'))
i_file = 0
n_file = len(files)

n = np.zeros((n_file, mlev, nlev))
m = np.zeros((n_file, mlev))
z = np.zeros((n_file, nlev))
t = np.zeros((n_file, nlev))
for f in files:
    data = np.loadtxt(f)
    print os.path.basename(f)
    for i in range(0, len(data[:,1])):
        n[i_file, i/nlev, i % nlev] = data[i, 0]
        m[i_file, i/nlev] = data[i, 1]
        z[i_file, i % nlev] = data[i, 2]
        t[i_file, i % nlev] = data[i, 3]*yr
    i_file = i_file+1


# redshift plots
print 'plotting as function of redshift'
rate_z = np.zeros((n_file, nlev-1))
for j_file in range(0, n_file):
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', files[j_file])
    for i in range(0, nlev-1):
        rate_z[j_file, i] = sum(n[j_file, :, i])/(z[j_file, i+1]-z[j_file, i])/(t[j_file, i]-t[j_file, i+1])
    plt.plot(z[j_file, :-1], rate_z[j_file], label=(r'$M_{min}=$'+paras[1]+\
        r'$M_{\odot}$'+'\n'+r'$\eta=$'+paras[3]))
    # '\n'+r'$M_{max}=$'+paras[2]+r'$M_{\odot}$'+


plt.ylabel(r'$\frac{d\dot{N}}{dz}[yr^{-1}]$', size=20)
plt.xlabel(r'$z$')
plt.xscale('linear')
plt.xlim(0, 35)
# print 'total number of CCSN: '+str(sum(n))
# plt.yscale('log')
plt.legend(bbox_to_anchor=(1.4, 1))
plt.title(r'Supernova Rates in one Milkyway-like Galaxy')
plt.savefig('../plots/both/CCSN_z.jpg', bbox_inches='tight')
plt.show()
plt.clf()

