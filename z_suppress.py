"""Author: M. Magg
Code for fast plotting Ba. project output data.
To be copied and modified for every application
"""
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import re
from copy import deepcopy

n_eta = 3
n_mmin = 2
nlev = 256
mlev = 256


print 'reading data'
files = glob.glob(os.path.join('output_mmax', 'z_supp*'))
i_file = 0
n_file = len(files)

z = np.zeros((n_file, nlev))
m = np.zeros((n_file, nlev))
m_crit = np.zeros((n_file, nlev))
t_dyn = np.zeros((n_file, nlev))
z_enr = np.zeros((n_file, nlev))
LW = np.zeros((n_file, nlev))
anys = np.zeros((n_file, nlev))

for f in files:
    print os.path.basename(f)
    data = np.loadtxt(f)
    z[i_file, :] = data[:, 0]
    m[i_file, :] = data[:, 1]
    m_crit[i_file, :] = data[:, 3]
    t_dyn[i_file, :] = data[:, 5]
    z_enr[i_file, :] = data[:, 7]
    LW[i_file, :] = data[:, 9]
    anys[i_file, :] = data[:, 11]
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', os.path.basename(files[i_file]))
    i_file = i_file + 1


print 'plotting'
plt.plot(False, False, color='white', label=(r'For $M_{max}=$'+str(float(paras[2]))+r'$M_{\odot}$'))
for j_file in range(n_file):
    all_sup = anys[j_file, :]+m_crit[j_file, :]
    test_array = (all_sup > 0)
    all_sup = all_sup[test_array]
    fraction_of = all_sup
    z_curr = z[j_file, test_array]
    m_curr = m[j_file, test_array]
    m_crit_curr = m_crit[j_file, test_array]
    t_dyn_curr = t_dyn[j_file, test_array]
    z_enr_curr = z_enr[j_file, test_array]
    LW_curr = LW[j_file, test_array]
    anys_curr = anys[j_file, test_array]
    all_ex_m = LW[j_file, test_array ]+ z_enr[j_file, test_array]+t_dyn[j_file, test_array]
    more = LW[j_file, test_array]+ z_enr[j_file, test_array]+t_dyn[j_file, test_array]-anys[j_file, test_array]
    renorm = np.zeros(len(z_curr))
    for i in range(len(z_curr)):
        if all_ex_m[i]>0:
            renorm[i] = (anys_curr[i]-more[i])/all_ex_m[i]
        else:
            renorm[i] = 1
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', os.path.basename(files[j_file]))
    supp =  t_dyn[j_file, test_array]*renorm/fraction_of
    plt.plot(z_curr, supp, color='lightblue', label=(r'$t_{dyn}$'))
    plt.fill_between(z_curr, supp, 1.0e-6, facecolor='lightblue')#, interpolate=True)
    last = deepcopy(supp)
    supp = LW[j_file, test_array]*renorm/fraction_of +supp
    plt.plot(z_curr, supp, color='purple', label=(r'$LW$'))
    plt.fill_between(z_curr, supp, last, facecolor='purple')#, interpolate=True)
    last = deepcopy(supp)
    supp = z_enr[j_file, test_array]*renorm/fraction_of + supp
    plt.plot(z_curr, supp, color='green', label=(r'$Z_{enr}$'))
    plt.fill_between(z_curr, supp, last, facecolor='green')#, interpolate=True)
    last = deepcopy(supp)
    supp = anys[j_file, test_array]/fraction_of
    plt.plot(z_curr, supp, color='red', label=(r'$Z_{enr}/t_{dyn}/LW$'))
    plt.fill_between(z_curr, supp, last, facecolor='red')#, interpolate=True)
    last = deepcopy(supp)
    supp =m_crit[j_file, test_array]/fraction_of + supp
    plt.plot(z_curr, supp, color='blue', label=(r'$m_{crit}$'))
    plt.fill_between(z_curr, supp, last, facecolor='blue')#, interpolate=True)
    plt.ylabel(r'gas mass fraction', size=16)
    plt.xlabel(r'redshift $z$', size = 16)
    plt.xlim(min(z_curr),max(z_curr))
    plt.ylim(1.0e-3,1.0)
    #plt.yscale('log', nonposy='clip')
    plt.legend(bbox_to_anchor=(1.3, 0.5))
    #plt.grid(b=True, which='both', color='0.65',linestyle='-')
    plt.savefig('z_supp_mmax'+paras[2]+'mmin'+paras[1]+'.jpg', bbox_inches='tight')
    #plt.show()
    plt.clf()

