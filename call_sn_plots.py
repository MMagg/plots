"""Author: M. Magg
Code for fast plotting Ba. project output data.
To be copied and modified for every application
"""
import os
directory= os.path.join('..', '..', 'public')
print 'supernovae volume plots'
execfile(os.path.join(directory,'sn_vol.py'))
print 'supernovae angle plots'
execfile(os.path.join(directory,'sn_angle.py'))
print 'supernovae cumulativ angle plots'
execfile(os.path.join(directory,'sn_angle_cumu.py'))
print 'supernovae location plots'
execfile(os.path.join(directory,'sn_M.py'))