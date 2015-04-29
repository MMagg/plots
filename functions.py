import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumtrapz
from scipy.integrate import quad
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
V = 1000 #Mpc^3
rad_to_arcmin = 10800/np.pi

def dr_dz(z):
    y = c/H_0/km_to_cm/np.sqrt(omega_m*(1+z)**3+omega_l)
    return y


def IMF(M):
    M_char = 40 # M_sun
    dn_dlogM = M**(-1.3)*np.exp(-(M_char/M)**1.6)
    return dn_dlogM/M

def M_IMF(M):
    M_char = 40 # M_sun
    dn_dlogM = M**(-1.3)*np.exp(-(M_char/M)**1.6)
    return dn_dlogM


def plot_hummel_cumulativ():

    print 'plotting comparision [Hummel]'
    files_hummel = glob.glob(os.path.join('..', '..', 'public', 'formation-rate_*'))
    files_hummel.sort()

    for f in files_hummel:
        data = np.loadtxt(f)
        print os.path.basename(f)
        dn_dt = data[:, 6]
        z = data[:, 1]
        rate = (dn_dt)*10
        cum_rate = cumtrapz(rate, x=z)
        paras = re.split('formation-rate_|.dat', os.path.basename(f))
        plt.plot(z[:-1], max(cum_rate)-cum_rate, '-.', label=('Hummel et al. 2012 '+paras[1]))


def plot_hummel_angle():

    print 'plotting comparision [Hummel]'
    files_hummel = glob.glob(os.path.join('..', '..', 'public', 'formation-rate_*'))
    files_hummel.sort()

    for f in files_hummel:
        data = np.loadtxt(f)
        print os.path.basename(f)
        dn_dt = data[:, 6]
        z = data[:, 1]
        rate = (dn_dt)*10
        paras = re.split('formation-rate_|.dat', os.path.basename(f))
        plt.plot(z, rate, '-.', label=('Hummel et al. 2012 '+paras[1]))



def plot_hummel_vol():

    print 'plotting comparision [Hummel]'
    files_hummel = glob.glob(os.path.join('..', '..', 'public', 'formation-rate_*'))
    files_hummel.sort()

    for f in files_hummel:
        data = np.loadtxt(f)
        print os.path.basename(f)
        dn_dt = data[:, 5]
        z = data[:, 1]
        rate = (dn_dt)
        paras = re.split('formation-rate_|.dat', os.path.basename(f))
        plt.plot(z, rate, '-.', label=('Hummel et al. 2012 '+paras[1]))



def sfr_cc_cumulativ():

    print 'reading data'
    files_sfr = glob.glob(os.path.join('..', '..', 'SFR_from_UCSD', 'SFR_*'))
    files_sfr.sort()
    M_tot, M_tot_err = quad(M_IMF, 0, np.inf)
    f_sn = (quad(IMF, 8., 40.))[0]/M_tot
    for f in files_sfr:
        data = np.loadtxt(f, skiprows=1)
        print os.path.basename(f)
        SFR = data[:, 2]
        z = data[:, 0]
        t = data[:, 1]*yr*10**6
        temp = cumtrapz(dr_dz(z), x=z)
        z_0 = trapz(dr_dz(np.linspace(0, min(z), 1000)), x=np.linspace(0, min(z), 1000))
        r = np.hstack([temp+z_0, z_0])
        n_sn = SFR*f_sn
        rate = n_sn*r**2*dr_dz(z)/(rad_to_arcmin**2)*10 # /(z+1)
        cum_rate = cumtrapz(rate[:], x=z[:])
        paras = re.split('SFR_|.txt', os.path.basename(f))
        plt.plot(z[:-1], max(cum_rate)-cum_rate, ':', label=('From renaissance SFR '+paras[1]))

def sfr_pi_cumulativ():

    print 'reading data'
    M_char = 40 # M_sun
    files_sfr = glob.glob(os.path.join('..', '..', 'SFR_from_UCSD', 'SFR_*'))
    files_sfr.sort()
    M_tot, M_tot_err = quad(M_IMF, 0, np.inf)
    f_sn = (quad(IMF, 140., 260.))[0]/M_tot
    for f in files_sfr:
        data = np.loadtxt(f, skiprows=1)
        print os.path.basename(f)
        SFR = data[:, 2]
        z = data[:, 0]
        t = data[:, 1]*yr*10**6
        temp = cumtrapz(dr_dz(z), x=z)
        z_0 = trapz(dr_dz(np.linspace(0, min(z), 1000)), x=np.linspace(0, min(z), 1000))
        r = np.hstack([temp+z_0, z_0])
        n_sn = SFR*f_sn
        rate = n_sn*r**2*dr_dz(z)/(rad_to_arcmin**2)*10 # /(z+1)
        cum_rate = cumtrapz(rate[:], x=z[:])
        paras = re.split('SFR_|.txt', os.path.basename(f))
        plt.plot(z[:-1], max(cum_rate)-cum_rate, ':', label=('From renaissance SFR '+paras[1]))


def sfr_cc_angle():

    print 'reading data'
    files_sfr = glob.glob(os.path.join('..', '..', 'SFR_from_UCSD', 'SFR_*'))
    files_sfr.sort()
    M_tot, M_tot_err = quad(M_IMF, 0, np.inf)
    f_sn = (quad(IMF, 8., 40.))[0]/M_tot
    for f in files_sfr:
        data = np.loadtxt(f, skiprows=1)
        print os.path.basename(f)
        SFR = data[:, 2]
        z = data[:, 0]
        t = data[:, 1]*yr*10**6
        temp = cumtrapz(dr_dz(z), x=z)
        z_0 = trapz(dr_dz(np.linspace(0, min(z), 1000)), x=np.linspace(0, min(z), 1000))
        r = np.hstack([temp+z_0, z_0])
        n_sn = SFR*f_sn
        rate = n_sn*r**2*dr_dz(z)/(rad_to_arcmin**2)*10 # /(z+1)
        paras = re.split('SFR_|.txt', os.path.basename(f))
        plt.plot(z, rate, ':', label=('From renaissance SFR '+paras[1]))

def sfr_pi_angle():

    print 'reading data'
    M_char = 40 # M_sun
    files_sfr = glob.glob(os.path.join('..', '..', 'SFR_from_UCSD', 'SFR_*'))
    files_sfr.sort()
    M_tot, M_tot_err = quad(M_IMF, 0, np.inf)
    f_sn = (quad(IMF, 140., 260.))[0]/M_tot
    for f in files_sfr:
        data = np.loadtxt(f, skiprows=1)
        print os.path.basename(f)
        SFR = data[:, 2]
        z = data[:, 0]
        t = data[:, 1]*yr*10**6
        temp = cumtrapz(dr_dz(z), x=z)
        z_0 = trapz(dr_dz(np.linspace(0, min(z), 1000)), x=np.linspace(0, min(z), 1000))
        r = np.hstack([temp+z_0, z_0])
        n_sn = SFR*f_sn
        rate = n_sn*r**2*dr_dz(z)/(rad_to_arcmin**2)*10 # /(z+1)
        paras = re.split('SFR_|.txt', os.path.basename(f))
        plt.plot(z, rate, ':', label=('From renaissance SFR '+paras[1]))

def sfr_cc_vol():

    print 'reading data'
    files_sfr = glob.glob(os.path.join('..', '..', 'SFR_from_UCSD', 'SFR_*'))
    files_sfr.sort()
    M_tot, M_tot_err = quad(M_IMF, 0, np.inf)
    f_sn = (quad(IMF, 8., 40.))[0]/M_tot
    for f in files_sfr:
        data = np.loadtxt(f, skiprows=1)
        print os.path.basename(f)
        SFR = data[:, 2]
        z = data[:, 0]
        t = data[:, 1]*yr*10**6
        temp = cumtrapz(dr_dz(z), x=z)
        z_0 = trapz(dr_dz(np.linspace(0, min(z), 1000)), x=np.linspace(0, min(z), 1000))
        r = np.hstack([temp+z_0, z_0])
        n_sn = SFR*f_sn
        rate = n_sn *(z+1)
        paras = re.split('SFR_|.txt', os.path.basename(f))
        plt.plot(z, rate, ':', label=('From renaissance SFR '+paras[1]))

def sfr_pi_vol():

    print 'reading data'
    M_char = 40 # M_sun
    files_sfr = glob.glob(os.path.join('..', '..', 'SFR_from_UCSD', 'SFR_*'))
    files_sfr.sort()
    M_tot, M_tot_err = quad(M_IMF, 0, np.inf)
    f_sn = (quad(IMF, 140., 260.))[0]/M_tot
    for f in files_sfr:
        data = np.loadtxt(f, skiprows=1)
        print os.path.basename(f)
        SFR = data[:, 2]
        z = data[:, 0]
        t = data[:, 1]*yr*10**6
        temp = cumtrapz(dr_dz(z), x=z)
        z_0 = trapz(dr_dz(np.linspace(0, min(z), 1000)), x=np.linspace(0, min(z), 1000))
        r = np.hstack([temp+z_0, z_0])
        n_sn = SFR*f_sn
        rate = n_sn*(z+1)
        paras = re.split('SFR_|.txt', os.path.basename(f))
        plt.plot(z, rate, ':', label=('From renaissance SFR '+paras[1]))