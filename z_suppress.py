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


print 'reading data'
files = glob.glob(os.path.join('..', 'Code', 'output_vanilla', 'z_supp*'))
i_file = 0
n_file = len(files)

z = np.zeros((n_file, nlev))
m = np.zeros((n_file, nlev))
m_std = np.zeros((n_file, nlev))
m_crit = np.zeros((n_file, nlev))
m_crit_std = np.zeros((n_file, nlev))
t_dyn = np.zeros((n_file, nlev))
t_dyn_std = np.zeros((n_file, nlev))
z_enr = np.zeros((n_file, nlev))
z_enr_std = np.zeros((n_file, nlev))
LW = np.zeros((n_file, nlev))
LW_std = np.zeros((n_file, nlev))
more = np.zeros((n_file, nlev))
more_std = np.zeros((n_file, nlev))

for f in files:
    print os.path.basename(f)
    data = np.loadtxt(f)
    z[i_file, :] = data[:, 0]
    m[i_file, :] = data[:, 13]
    m_std[i_file, :] = data[:, 14]
    m_crit[i_file, :] = data[:, 3]
    m_crit_std[i_file, :] = data[:, 4]
    t_dyn[i_file, :] = data[:, 5]
    t_dyn_std[i_file, :] = data[:, 6]
    z_enr[i_file, :] = data[:, 7]
    z_enr_std[i_file, :] = data[:, 7]
    LW[i_file, :] = data[:, 9]
    LW_std[i_file, :] = data[:, 10]
    more[i_file, :] = data[:, 11]
    more_std[i_file, :] = data[:, 12]
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', os.path.basename(files[i_file]))
    i_file = i_file + 1


print 'plotting'
plt.plot(False, False, color='white', label=(r'For $M_{max}=$'+str(float(paras[2]))+r'$M_{\odot}$'))
for j_file in range(n_file):
    all_sup = more[j_file, :]
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', os.path.basename(files[j_file]))
    supp =  t_dyn[j_file, :]/all_sup
    plt.plot(z[j_file, :], supp, label=(r'$t_{dyn}$'))
    supp = LW[j_file, :]/all_sup #+supp
    plt.plot(z[j_file, :], supp, label=(r'$LW$'))
    supp = z_enr[j_file, :]/all_sup #+ supp
    plt.plot(z[j_file, :], supp, label=(r'$Z_{enr}$'))
    supp = more[j_file, :]/all_sup #+ supp
    plt.plot(z[j_file, :], supp, label=(r'$any$'))
    supp =m_crit[j_file, :]/all_sup #+ supp
    plt.plot(z[j_file, :], supp, label=(r'$m_{crit}$'))
    plt.ylabel(r'gas mass fraction', size=16)
    plt.xlabel(r'redshift $z$', size = 16)
    plt.xscale('linear')
    plt.xlim(0, 35)
    #plt.ylim(1.0e-4,10.0)
    plt.yscale('log')
    plt.legend(bbox_to_anchor=(1.3, 0.5))
    plt.grid(b=True, which='both', color='0.65',linestyle='-')
    plt.savefig('../high_n_data/plots/z_supp_eta'+paras[3]+'.jpg', bbox_inches='tight')
    plt.show()
    plt.clf()

