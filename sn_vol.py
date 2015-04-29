"""Author: M. Magg
Code for fast plotting Ba. project output data.
To be copied and modified for every application
"""
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import re
from functions import plot_hummel_vol
import functions

nlev = 256
mlev = 256
yr = (31557600)**(-1)
V = 1000 # MPc^3

print ('reading core collapse sn data')
files_cc = glob.glob(os.path.join('output_sn', 'sn_rates', 'ccsn*'))
i_file = 0
n_file = len(files_cc)

n_cc = np.zeros((n_file, mlev, nlev))
m_cc = np.zeros((n_file, mlev))
z_cc = np.zeros((n_file, nlev))
t_cc = np.zeros((n_file, nlev))
for f in files_cc:
    data = np.loadtxt(f)
    print (os.path.basename(f))
    for i in range(0, len(data[:,1])):
        n_cc[i_file, i/nlev, i % nlev] = data[i, 0]
        m_cc[i_file, i/nlev] = data[i, 1]
        z_cc[i_file, i % nlev] = data[i, 2]
        t_cc[i_file, i % nlev] = data[i, 3]*yr
    i_file = i_file+1

print ('reading pair instability sn data...')
files_pi = glob.glob(os.path.join('output_sn', 'sn_rates', 'pisn*'))
i_file = 0
n_file = len(files_pi)

n_pi = np.zeros((n_file, mlev, nlev))
m_pi = np.zeros((n_file, mlev))
z_pi = np.zeros((n_file, nlev))
t_pi = np.zeros((n_file, nlev))
for f in files_pi:
    data = np.loadtxt(f)
    print (os.path.basename(f))
    for i in range(0, len(data[:,1])):
        n_pi[i_file, i/nlev, i % nlev] = data[i, 0]
        m_pi[i_file, i/nlev] = data[i, 1]
        z_pi[i_file, i % nlev] = data[i, 2]
        t_pi[i_file, i % nlev] = data[i, 3]*yr
    i_file = i_file+1


# redshift plots
print ('plotting CC as function of redshift...')
rate_z_cc = np.zeros((n_file, nlev-1))
for j_file in range(0, n_file):
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', os.path.basename(files_cc[j_file]))
    for i in range(0, nlev-1):
        rate_z_cc[j_file, i] = sum(n_cc[j_file, :, i])/(t_cc[j_file, i]-t_cc[j_file, i+1])/V
    plt.plot(z_cc[j_file, :-1], rate_z_cc[j_file], label=(r'$M_{max}=$'+str(float(paras[2]))+\
        r'$M_{\odot}$'+'\n'+r'$\eta=$'+str(float(paras[3]))))
    # '\n'+r'$M_{max}=$'+paras[2]+r'$M_{\odot}$'+

# plt.grid(b=True, which='both', color='0.65',linestyle='-')
functions.sfr_cc_vol()
plt.ylabel(r'$\dot{n}[MPc^{-3}yr^{-1}]$', size=20)
plt.xlabel(r'$z$')
plt.xscale('linear')
plt.xlim(0, 35)
# plt.ylim(1.0e-7,0.1)
# # print 'total number of CCSN: '+str(sum(n))
plt.yscale('log')
plt.legend(bbox_to_anchor=(1.7, 1.0))
plt.title(r'Core Collapse Supernova Rate Denstity')
plt.savefig('CCSN_vol.eps', bbox_inches='tight')
# plt.show()
plt.clf()

# redshift plots
plot = False
print ('plotting PI as function of redshift...')
rate_z_pi = np.zeros((n_file, nlev-1))
for j_file in range(0, n_file):
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', os.path.basename(files_pi[j_file]))
    if (sum(sum(n_pi[j_file, :, :])) == 0):
        continue
    plot = True
    for i in range(0, nlev-1):
        rate_z_pi[j_file, i] = sum(n_pi[j_file, :, i])/(t_pi[j_file, i]-t_pi[j_file, i+1])/V
    plt.plot(z_pi[j_file, :-1], rate_z_pi[j_file], label=(r'$M_{max}=$'+str(float(paras[2]))+\
        r'$M_{\odot}$'+'\n'+r'$\eta=$'+str(float(paras[3]))))
    # '\n'+r'$M_{max}=$'+paras[2]+r'$M_{\odot}$'+

if plot:
    # plt.grid(b=True, which='both', color='0.65',linestyle='-')
    functions.sfr_pi_vol()
    plot_hummel_vol()
    plt.ylabel(r'$\dot{n}[MPc^{-3}yr^{-1}]$', size=20)
    plt.xlabel(r'$z$')
    plt.xscale('linear')
    plt.xlim(0, 35)
    plt.ylim(1.0e-11, 2.e-6)
    # plt.ylim(1.0e-8,0.01)
    # # print 'total number of CCSN: '+str(sum(n))
    plt.yscale('log')
    plt.legend(bbox_to_anchor=(1.7, 1.0))
    plt.title(r'Pair Instability Supernova Rate Density')
    plt.savefig('PISN_vol.eps', bbox_inches='tight')
    # plt.show()
    plt.clf()
else:
    print 'NO PISN RECORDED'

