"""Author: M. Magg
Code for fast plotting Ba. project output data.
To be copied and modified for every application
"""
import numpy as np
import matplotlib.pyplot as plt

nlev = 256
mlev = 256
yr = (31557600 )**(-1)

#vanilla
print 'reading flat IMF'
N = 50.
full_v = np.zeros((3, mlev*nlev))
n_v = np.zeros((mlev, nlev))
m_v = np.zeros(mlev)
z_v = np.zeros(nlev)
dt_v = np.zeros(nlev)
first = True
i = 0
f = open("../imf_test/output_vanilla/CCSN.dat", 'r')
for line in f:
    line = line.strip()
    colls = line.split()
    if first:
        first = False
    else:
        n_v[i/nlev, i % nlev] = (float(colls[0]))/N
        m_v[i/nlev] = (float(colls[1]))
        z_v[i % nlev] = (float(colls[2]))
        dt_v[i % nlev] = (float(colls[3]))*yr
        full_v[:, i] = np.array([float(colls[0])/N, float(colls[1]),
                               float(colls[2])])
        i = i+1
f.close()

n_z_v = np.zeros(nlev)
for i in range(0, len(n_z_v)):
    n_z_v[i] = sum(n_v[:, i])

n_m_v = np.zeros(mlev)
for i in range(0, len(n_m_v)):
    n_m_v[i] = sum(n_v[i, :])

m_log_v = np.log(m_v[1:len(m_v)]/m_v[:len(m_v)-1])


# slope
print 'reading Salpeter IMF'
N = 50.
full_s = np.zeros((3, mlev*nlev))
n_s = np.zeros((mlev, nlev))
m_s = np.zeros(mlev)
z_s = np.zeros(nlev)
dt_s = np.zeros(nlev)
first = True
i = 0
f = open("../imf_test/output_slope/CCSN.dat", 'r')
for line in f:
    line = line.strip()
    colls = line.split()
    if first:
        first = False
    else:
        n_s[i/nlev, i % nlev] = (float(colls[0]))/N
        m_s[i/nlev] = (float(colls[1]))
        z_s[i % nlev] = (float(colls[2]))
        dt_s[i % nlev] = (float(colls[3]))*yr
        full_s[:, i] = np.array([float(colls[0])/N, float(colls[1]),
                               float(colls[2])])
        i = i+1

n_z_s = np.zeros(nlev)
for i in range(0, len(n_z_s)):
    n_z_s[i] = sum(n_s[:, i])

n_m_s = np.zeros(mlev)
for i in range(0, len(n_m_s)):
    n_m_s[i] = sum(n_s[i, :])

m_log_s = np.log(m_s[1:len(m_s)]/m_s[:len(m_s)-1])

# plots Mass
print 'plotting as function of mass'
plt.plot(m_v[:-1], n_m_v[:-1]/m_log_v, label='Logarithmically Flat IMF')
plt.plot(m_s[:-1], n_m_s[:-1]/m_log_s, label='Salpeter IMF')
plt.ylabel(r'$\frac{dN}{dM} [M_\odot^{-1}]$', size=20)
plt.xlabel(r'$M[M_\odot]$')
# print 'total number of CCSN: '+str(sum(n))
plt.xscale('log')
plt.xlim(7, 100)
# plt.yscale('log')
plt.legend(bbox_to_anchor=(1.2, 1))
plt.title(r'Counted Supernovae logartithmic mass')
plt.savefig('../plots/both/CCSN_m.jpg', bbox_inches='tight')
plt.clf()

print 'plotting as function of redshift'
plt.plot(z_v[:-1], n_z_v[:-1]/(z_v[1:]-z_v[:-1]), label='Logarithmically Flat IMF')
plt.plot(z_s[:-1], n_z_s[:-1]/(z_s[1:]-z_s[:-1]), label='Salpeter IMF')
plt.ylabel(r'$\frac{dN}{dz}$', size=20)
plt.xlabel(r'$z$')
plt.xscale('linear')
plt.xlim(0, 30)
# print 'total number of CCSN: '+str(sum(n))
# plt.yscale('log')
plt.legend(bbox_to_anchor=(1.1, 1))
plt.title(r'Counted Supernovae per unit redshift')
plt.savefig('../plots/both/CCSN_z.jpg', bbox_inches='tight')
plt.clf()

print 'colorbar plots'
# cbar plots

n_map_v = n_v[:-1, :-1]/(dt_v[1:]*(m_v[1:]-m_v[:-1]))
n_map_s = n_s[:-1, :-1]/(dt_s[1:]*(m_s[1:]-m_s[:-1]))

from matplotlib.colors import LogNorm
plt.figure(figsize=(24, 8))
plt.subplot(1, 2, 1)
plt.pcolor(z_v[:-1], m_v[:-1], n_map_v, vmin=0, vmax=n_map_v.max())
plt.ylim(8, 42)
plt.xlim(min(z_v), 40)
# plt.yscale('log')
plt.title('Logarithmically Flat IMF', size=25)
plt.ylabel(r'$m[M_{\odot}]$', size=30)
plt.xlabel(r'$z$', size=30)
cbar = plt.colorbar()
# cbar.get_major_formatter().set_powerlimits((0, 1))
cbar.set_label(r'$\frac{d N}{dm dz}[M_{\odot}^{-1}yr^{-1}]$', size=20)
# plt.savefig('../plots/CCSN_cbar_logflat.jpg', bbox_inches='tight')

plt.subplot(1, 2, 2)
plt.pcolor(z_s[:-1], m_s[:-1], n_map_s, vmin=0, vmax=n_map_s.max())
plt.ylim(8, 42)
plt.xlim(min(z_s), 40)
# plt.yscale('log')
plt.title('Salpeter IMF', size=25)
plt.suptitle('Number of core collaps SN \nper solar mass and year',
          y=1.05, size=25)
plt.ylabel(r'$m[M_{\odot}]$', size=30)
plt.xlabel(r'$z$', size=30)
cbar = plt.colorbar()
cbar.set_label(r'$\frac{d N}{dm dz}[M_{\odot}^{-1}yr^{-1}]$', size=20)
plt.savefig('../plots/both/CCSN_cbar.jpg', bbox_inches='tight')


