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

print 'reading core collapse sn data'
files_cc = glob.glob(os.path.join('..', 'work', 'output_vanilla', 'sn_rates', 'loc_ccsn_*'))
files_cc.sort()
i_file = 0
n_file = len(files_cc)

for f in files_cc:
    data = np.loadtxt(f)
    print os.path.basename(f)
    n_cc = data[:, 0]
    m_cc = data[:, 1]
    z_cc = data[:, 2]
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', os.path.basename(f))
    plt.scatter(z_cc, m_cc, s=0.02, label=(r'$M_{min}=$'+paras[1]+\
        r'$M_{\odot}$'+r'$\eta=$'+paras[3]))
    plt.ylabel(r'$M[M_{\odot}]$', size=20)
    plt.xlabel(r'$z$',  size=20)
    plt.legend(bbox_to_anchor=(1.6, 1))
    plt.title(r'Host Galaxy Mass distribution of Core Collapse SN')
    plt.xscale('linear')
    plt.xlim(0, 35)
    plt.yscale('log')
    plt.savefig('../plots/work/CCSN_distribution_eta'+str(paras[3])+'.jpg', bbox_inches='tight')
    plt.show()
    plt.clf()

    
    
"""print 'reading pair instability sn data'
files_pi = glob.glob(os.path.join('..', 'imf_test', 'output_vanilla', 'sn_rates', 'pisn*'))
files_pi.sort()
i_file = 0
n_file = len(files_pi)

n_pi = np.zeros((n_file, mlev, nlev))
m_pi = np.zeros((n_file, mlev))
z_pi = np.zeros((n_file, nlev))
t_pi = np.zeros((n_file, nlev))
for f in files_pi:
    data = np.loadtxt(f)
    print os.path.basename(f)
    for i in range(0, len(data[:,1])):
        n_pi[i_file, i/nlev, i % nlev] = data[i, 0]
        m_pi[i_file, i/nlev] = data[i, 1]
        z_pi[i_file, i % nlev] = data[i, 2]
        t_pi[i_file, i % nlev] = data[i, 3]*yr
    i_file = i_file+1"""


# redshift plots

    # '\n'+r'$M_{max}=$'+paras[2]+r'$M_{\odot}$'+



# print 'total number of CCSN: '+str(sum(n))
# plt.yscale('log')
# redshift plots
