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
tau_planck14 = 0.092
sig_tau14 = 0.013

tau_wmap = 0.084
sig_tau_wmap = 0.016




print 'reading data'
files = glob.glob(os.path.join('output_sn', 'z_eta_I*'))
files.sort()
i_file = 0
n_file = len(files)

z = np.zeros((n_file, nlev))
eta = np.zeros((n_file, nlev))
eta_std = np.zeros((n_file, nlev))

for f in files:
    print os.path.basename(f)
    data = np.loadtxt(f)
    z[i_file, :] = data[:, 0]
    eta[i_file, :] = data[:, 1]
    eta_std[i_file, :] = data[:, 2]
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', os.path.basename(files[i_file]))
    i_file = i_file + 1


print 'plotting'
#plt.plot(False, False, color='white', label=(r'For $M_{max}=$'+str(float(paras[2]))+r'$M_{\odot}$'))
for j_file in range(n_file):
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', os.path.basename(files[j_file]))
    plt.plot(z[j_file, :], eta[j_file, :], label=(r'$M_{max}=$'+str(float(paras[3]))+\
        r'$M_{\odot}$'+'\n'+r'$\eta=$'+str(float(paras[4]))))
    # '\n'+r'$M_{max}=$'+paras[2]+r'$M_{\odot}$'+
"""plt.plot(z[0, :], tau_arr14, label=('Planck 2014'), color='black', linestyle='-')
plt.plot(z[0, :], tau_arr14-sig_tau14, label=(r'$1\sigma$ error'), color='black', linestyle='-.')
plt.plot(z[0, :], tau_arr14+sig_tau14, color='black', linestyle='-.')
plt.plot(z[0, :], tau_arrwmap, label=('WMAP 2009'), color='red', linestyle='-')
plt.plot(z[0, :], tau_arrwmap-sig_tau_wmap, label=(r'$1\sigma$ error'), color='red', linestyle='-.')
plt.plot(z[0, :], tau_arrwmap+sig_tau_wmap, color='red', linestyle='-.')"""


plt.ylabel(r'Effective Star Formation Efficiency  $\eta$', size=16)
plt.xlabel(r'redshift $z$', size = 16)
plt.xscale('linear')
plt.xlim(0, 35)
# plt.yscale('log')
plt.legend(bbox_to_anchor=(1.4, 1.0))
plt.grid(b=True, which='both', color='0.65',linestyle='-')
plt.savefig(os.path.join('eff_eta.eps'), bbox_inches='tight')
plt.savefig(os.path.join('eff_eta.jpg'), bbox_inches='tight')
#plt.show()
plt.clf()

