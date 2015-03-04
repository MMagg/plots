"""Author: M. Magg
Code for fast plotting Ba. project output data. 
To be copied and modified for every application
"""
import numpy as np
import matplotlib.pyplot as plt

print 'Logarithmically flat IMF:' 
m = []
n = []
first = True
f = open("../imf_test/output_vanilla/imf.dat", 'r')
for line in f:
    line = line.strip()
    colls = line.split()
    if first:
        first = False
    else:
        n.append(float(colls[0]))
        m.append(float(colls[1]))
n = np.array(n)
m = np.array(m)
n_new = n[:len(n)-1]
m_1 = m[:len(n)-1]
m_new = np.log(m[1:len(n)]/m[:len(n)-1])
plt.plot(m_1, n_new/m_new, label='Logarithmically Flat IMF')
print 'total number of stars: '+str(sum(n))
print 'which equals a total mass of '+str(int(sum(n*m)))+' Msun'

print '\nSalpeter IMF'
m = []
n = []
first = True
f = open("../imf_test/output_slope/imf.dat", 'r')
for line in f:
    line = line.strip()
    colls = line.split()
    if first:
        first = False
    else:
        n.append(float(colls[0]))
        m.append(float(colls[1]))
n = np.array(n)
m = np.array(m)
n_new = n[:len(n)-1]
m_1 = m[:len(n)-1]
m_new = np.log(m[1:len(n)]/m[:len(n)-1])
plt.plot(m_1, n_new/m_new, label='Salpeter IMF')
plt.ylabel(r'$\frac{dN}{d\log{M}}$', size=20)
plt.xlabel(r'$M[M_\odot]$')
print 'total number of stars: '+str(sum(n))
print 'which equals a total mass of '+str(int(sum(n*m)))+' Msun'
plt.xscale('log')
#plt.yscale('log')
plt.legend()
plt.title('POPIII IMF (by counting formed stars)')
plt.savefig('../plots/imf.jpg')
plt.show()
