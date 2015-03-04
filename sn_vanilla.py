"""Author: M. Magg
Code for fast plotting Ba. project output data.
To be copied and modified for every application
"""
import numpy as np
import matplotlib.pyplot as plt

nlev = 256
mlev = 256
full = np.zeros((3, mlev*nlev))
m = np.zeros(mlev)
z = np.zeros(nlev)
n = np.zeros((mlev, nlev))
print np.shape(np.array((m,z)))
first = True
i = 0
f = open("../imf_test/output_vanilla/CCSN.dat", 'r')
for line in f:
    line = line.strip()
    colls = line.split()
    if first:
        first = False
    else:
        n[i/nlev, i % nlev] = (float(colls[0]))
        m[i/nlev] = (float(colls[1]))
        z[i % nlev] = (float(colls[2]))
        full[:, i] = np.array([float(colls[0]), float(colls[1]),
                               float(colls[2])])
        i = i+1


n_z = np.zeros(nlev)
for i in range(0, len(n_z)):
    n_z[i] = sum(n[:, i])

n_m = np.zeros(mlev)
for i in range(0, len(n_m)):
    n_m[i] = sum(n[i, :])

m_log = np.log(m[1:len(m)]/m[:len(m)-1])
print 'dn/dlogm'

plt.plot(m[:-1], n_m[:-1]/m_log, label='Logarithmically Flat IMF')
plt.ylabel(r'$\frac{dN}{d\log{M}}$', size=20)
plt.xlabel(r'$M[M_\odot]$')
# print 'total number of CCSN: '+str(sum(n))
plt.xscale('log')
plt.xlim(1, 60)
# plt.yscale('log')
plt.legend()
plt.title('Counted Supernovae')
plt.savefig('../plots/vanilla/CCSN_m.jpg', bbox_inches='tight')
plt.clf()
print 'dn/dz'
plt.plot(z[:-1], n_z[:-1]/(z[1:]-z[:-1]), label='Logarithmically Flat IMF')
plt.ylabel(r'$\frac{dN}{dz}$', size=20)
plt.xlabel(r'$z$')
plt.xscale('linear')
plt.xlim(0, 30)
# print 'total number of CCSN: '+str(sum(n))
# plt.yscale('log')
plt.legend()
plt.title('Counted Supernovae')
plt.savefig('../plots/vanilla/CCSN_z.jpg', bbox_inches='tight')
plt.clf()

# creating 2d_supernova "map"

n_map = n[:-1, :-1]/(m_log*(z[1:]-z[:-1]))

"""
# plotting colobar

from matplotlib.colors import LogNorm
plt.figure(figsize=(10, 8))
plt.pcolor(z[:-1], m[:-1], n_map, vmin=0, vmax=n_map.max())
plt.ylim(8, 42)
plt.xlim(min(z), 40)
plt.yscale('log')
plt.title('Number of Corecollaps SN per \n logarithmic mass and per redshift',
          y=1.05, size=25)
plt.ylabel(r'$m[M_{\odot}]$', size=30)
plt.xlabel(r'$z$', size=30)
cbar = plt.colorbar()
cbar.set_label(r'$\frac{d N}{dlog(m) dz}$', size=20)
plt.savefig('../plots/vanilla/CCSN_cbar.jpg', bbox_inches='tight')
"""

# plotting 3d
print "3D"
print np.meshgrid([10,20],[30,40])
zz, mm = np.meshgrid(z[:-1], m[:-1])
from mpl_toolkits.mplot3d.axes3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection='3d')
# ax.contourf3D(full[1,:], full[2,:], full[0,:])
# ax.bar(full[2,:], full[0,:], full[1,:], zdir = 'x')
n_map[n_map == 0] = 'NAN'
ax.plot_surface(mm, zz, n_map, shade=False)
ax.set_xlim3d(0, 40)
ax.set_ylim3d(2, 30)
# ax.set_xscale('log')
ax.set_zlabel(r'$\frac{d N}{dlog(m) dz}$', size=30)
ax.set_ylabel(r'$z$', size=30)
ax.set_xlabel(r'$m[M_{\odot}]$', size=30)
plt.savefig('../plots/vanilla/CCSN_3d.jpg', bbox_inches='tight')
plt.show()
