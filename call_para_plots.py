"""Author: M. Magg
Code for fast plotting Ba. project output data.
To be copied and modified for every application
"""
import os
directory= os.path.join('..', '..', 'public')
print 'tau plots'
execfile(os.path.join(directory,'tau_res.py'))
print 'black hole plots'
execfile(os.path.join(directory,'mbh.py'))
print 'supression plots'
execfile(os.path.join(directory,'z_suppress.py'))
print 'metallicity plots'
execfile(os.path.join(directory,'z_Z.py'))
print 'effective eta  plots'
execfile(os.path.join(directory,'eff_eta.py'))