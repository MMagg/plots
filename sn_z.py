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
t_v = np.zeros(nlev)
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
        t_v[i % nlev] = (float(colls[3]))*yr
        full_v[:, i] = np.array([float(colls[0])/N, float(colls[1]),
                               float(colls[2])])
        i = i+1
f.close()



# slope
print 'reading Salpeter IMF'
N = 50.
full_s = np.zeros((3, mlev*nlev))
n_s = np.zeros((mlev, nlev))
m_s = np.zeros(mlev)
z_s = np.zeros(nlev)
t_s = np.zeros(nlev)
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
        t_s[i % nlev] = (float(colls[3]))*yr
        full_s[:, i] = np.array([float(colls[0])/N, float(colls[1]),
                               float(colls[2])])
        i = i+1


m_log_s = np.log(m_s[1:len(m_s)]/m_s[:len(m_s)-1])


# redshift plots
print 'plotting as function of redshift'

rate_z_v = np.zeros(nlev-1)
for i in range(0, nlev-1):
    rate_z_v[i] = sum(n_v[:, i])/(z_v[i+1]-z_v[i])/(t_v[i]-t_v[i+1])

rate_z_s = np.zeros(nlev-1)
for i in range(0, nlev-1):
    rate_z_s[i] = sum(n_s[:, i])/(z_s[i+1]-z_s[i])/(t_s[i]-t_s[i+1])

plt.plot(z_v[:-1], rate_z_v, label='Logarithmically Flat IMF')
plt.plot(z_s[:-1], rate_z_s, label='Salpeter IMF')
plt.ylabel(r'$\frac{d\dot{N}}{dz}[yr^{-1}]$', size=20)
plt.xlabel(r'$z$')
plt.xscale('linear')
plt.xlim(0, 35)
# print 'total number of CCSN: '+str(sum(n))
# plt.yscale('log')
plt.legend(bbox_to_anchor=(1.4, 1))
plt.title(r'Counted Supernovae per unit redshift and year')
plt.savefig('../plots/both/CCSN_z.jpg', bbox_inches='tight')
plt.show()
plt.clf()

