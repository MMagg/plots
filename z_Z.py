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
V = 30 #Mpc^3


z_Z_ref = np.loadtxt(os.path.join('..', '..', 'Code', 'Data', 'z_Z.dat'))

print 'reading data'
files = glob.glob(os.path.join('output_sn', 'z_Z_*'))
files.sort()
i_file = 0
n_file = len(files)

z = np.zeros((n_file, nlev))
Z_max = np.zeros((n_file, nlev))
Z_mean = np.zeros((n_file, nlev))
Z_max_std = np.zeros((n_file, nlev))
Z_mean_std = np.zeros((n_file, nlev))

for f in files:
    print os.path.basename(f)
    data = np.loadtxt(f)
    Z_max[i_file, :] = data[:, 3]
    Z_mean[i_file, :] = data[:, 1]
    Z_max_std[i_file, :] = data[:, 4]
    Z_mean_std[i_file, :] = data[:, 2]
    z[i_file, :] = data[:, 0]
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', os.path.basename(f))
    i_file = i_file + 1

colors =['black', 'blue', 'green', 'red', 'purple' ]
print 'plotting'
plt.plot(False, False, color = 'white', label=(r'Max and Mean Metallicity'))
plt.plot(False, False, color='white', label=(r'For $M_{max}=$'+str(float(paras[2]))+r'$M_{\odot}$'))
for j_file in range(3):
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', os.path.basename(files[j_file]))
    plt.plot(z[j_file, :], Z_max[j_file, :], color = colors[j_file], label=(r'$\eta=$'+str(float(paras[3]))))
    plt.plot(z[j_file, :], Z_mean[j_file, :], color = colors[j_file])
    # '\n'+r'$M_{max}=$'+paras[2]+r'$M_{\odot}$'+
plt.scatter(z_Z_ref[:, 0], z_Z_ref[:, 1], s=3, label=('observations'), color='red')
#plt.plot(z[0, :], tau_arr-sig_tau, label=(r'$1\sigma$ error'), color='black', linestyle='-.')
#plt.plot(z[0, :], tau_arr+sig_tau, color='black', linestyle='-.')


plt.ylabel(r'Metallicity $Z$', size=16)
plt.xlabel(r'redshift $z$', size = 16)
plt.xscale('linear')
plt.xlim(0, 35)
plt.legend(bbox_to_anchor=(1.6, 1.0))
plt.grid(b=True, which='both', color='0.65',linestyle='-')
plt.savefig('z_Z.eps', bbox_inches='tight')
plt.savefig('z_Z.jpg', bbox_inches='tight')
#plt.show()
plt.clf()

