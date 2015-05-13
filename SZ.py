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

nlev = 256
mlev = 256
V = 1000 #Mpc^3
E_sn = 1e53 # erg
eps = 0.8 # fraction of SN energy lost to cmb


# conversion factors
yr = (31557600)**(-1) #yr/s
rad_to_arcmin = 10800/np.pi
# constants
H_0 = 67.77 # km/s/Mpc
c = 3.0e10 # cm/s
km_to_cm = 1.0e5 # cm/km
omega_m = 0.3086
omega_l = 0.6914
k_B = 1.38e-23 #J/K
h = 6.63e-34 # Js
T_cmb = 2.7 # K

def g_x(nu):
    x =  h*nu/k_B/T_cmb
    g = x**4*np.exp(x)*(x/np.tanh(x/2.)-4.)/(np.exp(x)-1)**2
    return g

def compton_gamma(z,  nu, E_sn):
    gamma = 1.8e-2*(g_x(nu)/4.)*(E_sn/1e53)*(eps/0.5)*(z/20)**2
    return gamma

def int_E_t(E_sn, z):
    t_cool = 1.4e7*((1+z)/20)**(-4) # yr
    return E_sn*t_cool # yr*erg

def integrated_flux(rate, z, nu):
    temp = rate*compton_gamma(z[:-1],  nu, int_E_t(E_sn, z[:-1]))
    return temp

def dr(z):
    y = c/(H_0*km_to_cm)/np.sqrt(omega_m*(1+z)**3+omega_l)
    return y



print 'reading pair instability sn data'
files_pi = glob.glob(os.path.join('output_sn', 'sn_rates', 'pisn*'))
files_pi.sort()
i_file = 0
n_file = len(files_pi)

n_pi = np.zeros((n_file, mlev, nlev))
m_pi = np.zeros((n_file, mlev))
z_pi = np.zeros((n_file, nlev))
t_pi = np.zeros((n_file, nlev))
r_pi = np.zeros((n_file, nlev))

for f in files_pi:
    data = np.loadtxt(f)
    print os.path.basename(f)
    for i in range(0, len(data[:,1])):
        n_pi[i_file, i/nlev, i % nlev] = data[i, 0]
        m_pi[i_file, i/nlev] = data[i, 1]
        z_pi[i_file, i % nlev] = data[i, 2]
        t_pi[i_file, i % nlev] = data[i, 3]*yr
    temp = cumtrapz(dr(z_pi[i_file, :]), x=z_pi[i_file, :])
    z_0 = trapz(dr(np.linspace(0, z_pi[i_file, 0], 1000)), x=np.linspace(0, z_pi[i_file, 0], 1000))
    r_pi[i_file,:] = np.hstack([z_0, temp+z_0])
    i_file = i_file+1




# redshift plots
plot = False
print 'plotting as function of redshift'
rate_z_pi = np.zeros((n_file, nlev-1))
for j_file in range(0, n_file):
    if (sum(sum(n_pi[j_file, :, :])) == 0):
        continue
    paras = re.split('IMFmin|IMFmax|eta|slope|.dat', os.path.basename(files_pi[j_file]))
    plot = True
    for i in range(0, nlev-1):
        dN = sum(n_pi[j_file, :, i])
        dz = z_pi[j_file, i+1]-z_pi[j_file, i]
        dt = t_pi[j_file, i]-t_pi[j_file, i+1]
        dr = r_pi[j_file, i+1]-r_pi[j_file, i]
        rate_z_pi[j_file, i] = dN/dt/V/(z_pi[j_file, i]+1)*r_pi[j_file, i]**2*dr/dz/(rad_to_arcmin**2)*3600
    total_flux = []
    nu_array = np.linspace(50e9, 1e12, 10000)
    for nu in nu_array:
        flux = integrated_flux(rate_z_pi[j_file, :], z_pi[j_file, :], nu)
        total_flux.append(trapz(flux, x=z_pi[j_file, :-1]))
    total_flux = np.array(total_flux)
    plt.plot(nu_array/10**9,  total_flux/1.e6, label=(r'$M_{max}=$'+str(float(paras[2]))+\
        r'$M_{\odot}$'+'\n'+r'$\eta=$'+str(float(paras[3]))))



if plot:
    plt.ylabel(r'flux $\frac{\mathrm{mJy}}{\mathrm{deg}^2}$', size=20)
    plt.xlabel(r'$\nu[\mathrm{GHz}]$')
    plt.xscale('linear')
    plt.yscale('log')
    # plt.xlim(0, 35)
    # plt.ylim(1.e-8, 1.e-2)
    plt.yscale('log')
    plt.legend(bbox_to_anchor=(1.4, 1))
    plt.title(r'SZE from PISN')
    plt.savefig('SZ.eps', bbox_inches='tight')
    #plt.show()
    plt.clf()
else:
    print 'NO PISN RECORDED'
"""plt.plot(z_pi[j_file, :-1], rate_z_pi[j_file], label=(r'$M_{max}=$'+str(float(paras[2]))+\
        r'$M_{\odot}$'+'\n'+r'$\eta=$'+str(float(paras[3]))))
    functions.sfr_pi_angle()
    plot_hummel_angle()"""
