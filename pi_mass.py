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
j = 0
f = open("../imf_test/output_vanilla/sn_rates/pisn_IMFmin8.0E-01IMFmax5.0E+02eta2.0E-03slope0.0E+00.dat", 'r')
for line in f:
    line = line.strip()
    colls = line.split()
    if j>1:
        n_v[i/nlev, i % nlev] = (float(colls[0]))/N
        m_v[i/nlev] = (float(colls[1]))
        z_v[i % nlev] = (float(colls[2]))
        t_v[i % nlev] = (float(colls[3]))*yr
        full_v[:, i] = np.array([float(colls[0])/N, float(colls[1]),
                               float(colls[2])])
        i = i+1
    j = j+1
f.close()



# plots Mass

rate_m_v = np.zeros(mlev)
for i in range(0, mlev-1):
    rate_m_v[i] = sum(n_v[i, :])/(m_v[i+1]-m_v[i])

m_log_v = np.log(m_v[1:len(m_v)]/m_v[:len(m_v)-1])


print 'plotting as function of mass'
plt.plot(m_v[:-1], rate_m_v[:-1])
plt.ylabel(r'$\frac{dN}{dM} [M_\odot^{-1}]$', size=20)
plt.xlabel(r'$M[M_\odot]$')
# print 'total number of CCSN: '+str(sum(n))
plt.xlim(135, 270)
# plt.yscale('log')
# plt.legend(bbox_to_anchor=(1.2, 1))
plt.title(r'Counted Supernovae per mass')
plt.savefig('../plots/both/PISN_m.jpg', bbox_inches='tight')
plt.show()
plt.clf()
