"""Author: M. Magg
Code for fast plotting Ba. project output data. 
To be copied and modified for every application
"""
import numpy as np
import matplotlib.pyplot as plt

nlev=256
mlev=256
n = np.zeros((mlev, nlev))
m = np.zeros(mlev)
z = np.zeros(nlev)
first = True
i = 0
f = open("../imf_test/output_vanilla/CCSN.dat", 'r')
for line in f:
    line = line.strip()
    colls = line.split()
    if first:
        first = False
    else:
        n[i/nlev, i%nlev] = (float(colls[0]))
        m[i/nlev] = (float(colls[1]))
        z[i%nlev] = (float(colls[2]))
        i = i+1


n_z = np.zeros(nlev)
for i in range(0,len(n_z)):
    n_z[i] = sum(n[:,i])
    
m_log = np.log(m[1:len(m)]/m[:len(m)-1])
plt.plot(z[:-1], n_z[:-1]/m_log, label='Logarithmically Flat IMF')
plt.ylabel(r'$\frac{dN}{d\log{M}}$', size=20)
#plt.xlabel(r'$M[M_\odot]$')
plt.xlabel(r'$z$')
print 'total number of CCSN: '+str(sum(n))
plt.xscale('log')
#plt.yscale('log')
plt.legend()
plt.title('Counted Supernovae')
plt.savefig('../plots/CCSN.jpg')
plt.show()
