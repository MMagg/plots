"""Author: M. Magg
Code for fast plotting Ba. project output data.
To be copied and modified for every application
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumtrapz
from numpy import trapz
import glob
import os
import re
from functions import plot_hummel_angle
import functions
from scipy.optimize import curve_fit
nlev = 256
mlev = 256
yr = (31557600)**(-1) #yr/s
H_0 = 67.77 # km/s/Mpc
c = 3.0e10 # cm/s
km_to_cm = 1.0e5 # cm/km
omega_m = 0.3086
omega_l = 0.6914
V = 1000 #Mpc^3
rad_to_arcmin = 10800/np.pi

print 'reading sn data'
files_cc = glob.glob(os.path.join('output_sn', 'sn_rates', 'ccsn*'))
files_cc.sort()
i_file = 0
n_file = len(files_cc)

def dr(z):
    y = c/(H_0*km_to_cm)/np.sqrt(omega_m*(1+z)**3+omega_l)
    return y


def imf(m, A):
    m_char = 40
    return A*m**(-1.35)

n_cc = np.zeros((n_file, mlev, nlev))
m_cc = np.zeros((n_file, mlev))
z_cc = np.zeros((n_file, nlev))
t_cc = np.zeros((n_file, nlev))
r_cc = np.zeros((n_file, nlev))

for f in files_cc:
    data = np.loadtxt(f)
    print os.path.basename(f)
    for i in range(0, len(data[:,1])):
        n_cc[i_file, i/nlev, i % nlev] = data[i, 0]
        m_cc[i_file, i/nlev] = data[i, 1]
        z_cc[i_file, i % nlev] = data[i, 2]
        t_cc[i_file, i % nlev] = data[i, 3]*yr
    temp = cumtrapz(dr(z_cc[i_file, :]), x=z_cc[i_file, :])
    z_0 = trapz(dr(np.linspace(0, z_cc[i_file, 0], 1000)), x=np.linspace(0, z_cc[i_file, 0], 1000))
    r_cc[i_file,:] = np.hstack([z_0, temp+z_0])
    # plt.plot(z_cc[i_file,:], r_cc[i_file, :])
    # plt.show()
    i_file = i_file+1

n_m = np.zeros((n_file, mlev))
for i_file in range(n_file):
    for i in range(0, mlev):
        n_m[i_file, i] = sum(n_cc[i_file, i, :])
    m_log = np.log(m_cc[i_file, 1:]/m_cc[i_file, :-1])
    plt.plot(m_cc[i_file, 1:], n_m[i_file, 1:]/m_log, label='IMF from counted stars')
    A_opt, A_cov = curve_fit(imf, m_cc[i_file, 1:], n_m[i_file, 1:]/m_log)
    plt.plot(m_cc[i_file, 1:], imf(m_cc[i_file, 1:], A_opt), label='Salpeter IMF')
    plt.ylabel(r'$\frac{dN}{d\log{M}}$', size=20)
    plt.xlabel(r'$M[M_\odot]$')
    # print 'total number of CCSN: '+str(sum(n))
    plt.yscale('log')
    plt.xlim(0.8, 1000)
    plt.xscale('log')
    plt.legend(bbox_to_anchor=(1.6, 1.0))
    plt.title('Counted Supernovae')
    plt.savefig('mass.jpg', bbox_inches='tight')
    plt.show()
    plt.clf()
