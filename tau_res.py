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
tau_planck14 = 0.092
sig_tau14 = 0.013

tau_wmap = 0.084
sig_tau_wmap = 0.016



tau_arr14 = np.zeros(nlev)
tau_arr14.fill(tau_planck14)

tau_arrwmap = np.zeros(nlev)
tau_arrwmap.fill(tau_wmap)


print 'reading data'
files = glob.glob(os.path.join('output_sn', 'z_tauIII*'))
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
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', os.path.basename(files[i_file]))
    i_file = i_file + 1


print 'plotting'
#plt.plot(False, False, color='white', label=(r'For $M_{max}=$'+str(float(paras[2]))+r'$M_{\odot}$'))
for j_file in range(n_file):
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', os.path.basename(files[j_file]))
    plt.plot(z[j_file, :], tau[j_file, :], label=(r'$M_{max}=$'+str(float(paras[2]))+\
        r'$M_{\odot}$'+'\n'+r'$\eta=$'+str(float(paras[3]))))
    # '\n'+r'$M_{max}=$'+paras[2]+r'$M_{\odot}$'+
plt.plot(z[0, :], tau_arr14, label=('Planck 2014'), color='black', linestyle='-')
plt.plot(z[0, :], tau_arr14-sig_tau14, label=(r'$1\sigma$ error'), color='black', linestyle='-.')
plt.plot(z[0, :], tau_arr14+sig_tau14, color='black', linestyle='-.')
plt.plot(z[0, :], tau_arrwmap, label=('WMAP 2009'), color='red', linestyle='-')
plt.plot(z[0, :], tau_arrwmap-sig_tau_wmap, label=(r'$1\sigma$ error'), color='red', linestyle='-.')
plt.plot(z[0, :], tau_arrwmap+sig_tau_wmap, color='red', linestyle='-.')


plt.ylabel(r'Optical depth  $\tau$', size=16)
plt.xlabel(r'redshift $z$', size = 16)
plt.xscale('linear')
plt.xlim(0, 35)
# plt.yscale('log')
plt.legend(bbox_to_anchor=(1.4, 1.0))
plt.grid(b=True, which='both', color='0.65',linestyle='-')
plt.savefig(os.path.join('tau.eps'), bbox_inches='tight')
plt.savefig(os.path.join('tau.jpg'), bbox_inches='tight')
#plt.show()
plt.clf()

