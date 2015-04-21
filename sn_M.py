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
files_cc = glob.glob(os.path.join('output_mmax', 'sn_rates', 'loc_ccsn_*'))
files_cc.sort()
i_file = 0
n_file = len(files_cc)

for f in files_cc:
    data = np.loadtxt(f)
    if len(data) == 0:
        print "no SN in", os.path.basename(f)
        continue
    print os.path.basename(f)
    n_cc = data[:, 0]
    m_cc = data[:, 1]
    z_cc = data[:, 2]
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', os.path.basename(f))
    plt.scatter(z_cc, m_cc, s=0.02, label=(r'$M_{max}=$'+paras[2]+\
        r'$M_{\odot}$'+r'$\eta=$'+paras[3]))
    plt.ylabel(r'$M[M_{\odot}]$', size=20)
    plt.xlabel(r'$z$',  size=20)
    plt.legend(bbox_to_anchor=(1.6, 1))
    plt.title(r'Host Galaxy Mass distribution of Core Collapse SN')
    plt.xscale('linear')
    plt.xlim(0, 35)
    plt.ylim(1.0e5,1.0e8)
    plt.yscale('log')
    plt.savefig('CCSN_distribution_eta'+str(paras[3])+'.jpg', bbox_inches='tight')
    # plt.show()
    plt.clf()

print 'reading pair instability sn data'
files_pi = glob.glob(os.path.join('output_mmax', 'sn_rates', 'loc_pisn_*'))
files_pi.sort()
i_file = 0
n_file = len(files_pi)

for f in files_pi:
    data = np.loadtxt(f)
    if len(data) == 0:
        print "no SN in", os.path.basename(f)
        continue
    print os.path.basename(f)
    n_pi = data[:, 0]
    m_pi = data[:, 1]
    z_pi = data[:, 2]
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', os.path.basename(f))
    plt.scatter(z_pi, m_pi, s=0.02, label=(r'$M_{max}=$'+paras[2]+\
        r'$M_{\odot}$'+r'$\eta=$'+paras[3]))
    plt.ylabel(r'$M[M_{\odot}]$', size=20)
    plt.xlabel(r'$z$',  size=20)
    plt.legend(bbox_to_anchor=(1.6, 1))
    plt.title(r'Host Galaxy Mass distribution of Pair Instability SN')
    plt.xscale('linear')
    plt.xlim(0, 40)
    plt.ylim(1.0e5,1.0e8)
    plt.yscale('log')
    plt.savefig('PISN_distribution_eta'+str(paras[3])+'.jpg', bbox_inches='tight')
    # plt.show()
    plt.clf()