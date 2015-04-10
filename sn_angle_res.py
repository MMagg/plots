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

nlev = 256
mlev = 256
yr = (31557600)**(-1) #yr/s
H_0 = 67.77 # km/s/Mpc
c = 3.0e10 # cm/s
km_to_cm = 1.0e5 # cm/km
omega_m = 0.3086
omega_l = 0.6914
V = 30 #Mpc^3
rad_to_arcmin = np.pi/10800

print 'reading core collapse sn data'
files_cc = np.array(glob.glob(os.path.join('..', 'compare_res', 'ccsn_I*')))
n_file = len(files_cc)
sort_para = np.zeros(n_file)
for i in range(n_file):
    temp = re.split('IMFmin|IMFmax|eta|slope|res|.dat', os.path.basename(files_cc[i]))
    sort_para [i] = float(temp[5])
files_cc=files_cc[np.argsort(sort_para)]


def dr(z):
    y = c/H_0/km_to_cm/np.sqrt(omega_m*(1+z)**3+omega_l)
    return y


n_cc = np.zeros((n_file, mlev, nlev))
m_cc = np.zeros((n_file, mlev))
z_cc = np.zeros((n_file, nlev))
t_cc = np.zeros((n_file, nlev))
r_cc = np.zeros((n_file, nlev))

i_file = 0
for f in files_cc:
    data = np.loadtxt(f)
    print os.path.basename(f)
    for i in range(0, len(data[:,1])):
        n_cc[i_file, i/nlev, i % nlev] = data[i, 0]
        m_cc[i_file, i/nlev] = data[i, 1]
        z_cc[i_file, i % nlev] = data[i, 2]
        t_cc[i_file, i % nlev] = data[i, 3]*yr
    print 'total number of CCSN', sum(sum(n_cc[i_file,:,:]))
    temp = cumtrapz(dr(z_cc[i_file, :]), x=z_cc[i_file, :])
    z_0 = trapz(dr(np.linspace(0, z_cc[i_file, 0], 1000)), x=np.linspace(0, z_cc[i_file, 0], 1000))
    r_cc[i_file,:] = np.hstack([z_0, temp+z_0])
    # plt.plot(z_cc[i_file,:], r_cc[i_file, :])
    # plt.show()
    i_file = i_file+1

print 'reading pair instability sn data'
files_pi = np.array(glob.glob(os.path.join('..', 'compare_res', 'pisn_I*')))
n_file = len(files_pi)
sort_para = np.zeros(n_file)
for i in range(n_file):
    temp = re.split('IMFmin|IMFmax|eta|slope|res|.dat', os.path.basename(files_pi[i]))
    sort_para [i] = float(temp[5])
files_pi=files_pi[np.argsort(sort_para)]

n_pi = np.zeros((n_file, mlev, nlev))
m_pi = np.zeros((n_file, mlev))
z_pi = np.zeros((n_file, nlev))
t_pi = np.zeros((n_file, nlev))
r_pi = np.zeros((n_file, nlev))


i_file = 0
for f in files_pi:
    data = np.loadtxt(f)
    print os.path.basename(f)
    for i in range(0, len(data[:,1])):
        n_pi[i_file, i/nlev, i % nlev] = data[i, 0]
        m_pi[i_file, i/nlev] = data[i, 1]
        z_pi[i_file, i % nlev] = data[i, 2]
        t_pi[i_file, i % nlev] = data[i, 3]*yr
    print 'total number of PISN', sum(sum(n_pi[i_file,:,:]))
    temp = cumtrapz(dr(z_pi[i_file, :]), x=z_pi[i_file, :])
    z_0 = trapz(dr(np.linspace(0, z_pi[i_file, 0], 1000)), x=np.linspace(0, z_pi[i_file, 0], 1000))
    r_pi[i_file,:] = np.hstack([z_0, temp+z_0])
    i_file = i_file+1


# redshift plots
print 'plotting CC as function of redshift'
rate_z_cc = np.zeros((n_file, nlev-1))
for j_file in range(0, n_file):
    paras = re.split('IMFmin|IMFmax|eta|slope|res|.dat', os.path.basename(files_cc[j_file]))
    for i in range(0, nlev-1):
        dN = sum(n_cc[j_file, :, i])
        dz = z_cc[j_file, i+1]-z_cc[j_file, i]
        dt = t_cc[j_file, i]-t_cc[j_file, i+1]
        dr = r_cc[j_file, i+1]-r_cc[j_file, i]
        rate_z_cc[j_file, i] = dN/dt/V*(z_cc[j_file, i]+1)**2*r_cc[j_file, i]**2*dr/dz/rad_to_arcmin**(-2)
    plt.plot(z_cc[j_file, :-1], rate_z_cc[j_file], label=(r'$res=$'+str(float(paras[5]))+\
      r' $N=$'+str(sum(sum(n_cc[j_file,:,:])))))
    # '\n'+r'$M_{max}=$'+paras[2]+r'$M_{\odot}$'+


plt.ylabel(r'$\frac{dN}{dt_{obs}dzd\Omega}[(arcmin^2yr)^{-1}]$', size=20)
plt.xlabel(r'$z$')
plt.xscale('linear')
plt.yscale('log')
plt.xlim(0, 35)
# print 'total number of CCSN: '+str(sum(n))
# plt.yscale('log')
plt.legend(bbox_to_anchor=(1.6, 1))
plt.title(r'Core Collapse Supernova Rates')
plt.savefig('../plots/res/CCSN_angle.jpg', bbox_inches='tight')
plt.show()
plt.clf()

# redshift plots
print 'plotting PI as function of redshift'
rate_z_pi = np.zeros((n_file, nlev-1))
for j_file in range(0, n_file):
    paras = re.split('IMFmin|IMFmax|eta|slope|res|.dat', os.path.basename(files_pi[j_file]))
    for i in range(0, nlev-1):
        dN = sum(n_pi[j_file, :, i])
        dz = z_pi[j_file, i+1]-z_pi[j_file, i]
        dt = t_pi[j_file, i]-t_pi[j_file, i+1]
        dr = r_pi[j_file, i+1]-r_pi[j_file, i]
        rate_z_pi[j_file, i] = dN/dt/V*(z_pi[j_file, i]+1)**2*r_pi[j_file, i]**2*dr/dz/rad_to_arcmin**(-2)
    plt.plot(z_pi[j_file, :-1], rate_z_pi[j_file], label=(r'$res=$'+str(float(paras[5]))+\
      r' $N=$'+str(sum(sum(n_pi[j_file,:,:])))))
    # '\n'+r'$M_{max}=$'+paras[2]+r'$M_{\odot}$'+


plt.ylabel(r'$\frac{dN}{dt_{obs}dzd\Omega}[(arcmin^2yr)^{-1}]$', size=20)
plt.xlabel(r'$z$')
plt.xscale('linear')
plt.yscale('log')
plt.xlim(0, 35)
# print 'total number of CCSN: '+str(sum(n))
# plt.yscale('log')
plt.legend(bbox_to_anchor=(1.6, 1))
plt.title(r'Pair Instability Supernova Rates')
plt.savefig('../plots/res/PISN_angle.jpg', bbox_inches='tight')
plt.show()
plt.clf()

