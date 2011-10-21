import sys, os

sys.path.append('./modules')
sys.path.append('../common/modules')

from tankshapes import gun, hull, constants as sconst

mytank = []

myhull = hull.hull_shape(sconst.id_hull_medium, (-20, -40), (40, 80))
mytank.append(myhull)

mygun = gun.gun_shape(sconst.id_gun_cannon, (-14, -38), sconst.layer_on_hull)
mytank.append(mygun)

mygun = gun.gun_shape(sconst.id_gun_cannon, (6, -38), sconst.layer_on_hull)
mytank.append(mygun)

import pickle
f = open('./pickled-tank.txt', 'w')
pickle.dump(mytank,f)

####

import sys, os

sys.path.append('./modules')
sys.path.append('../common/modules')

import pickle
f = open('./pickled-tank.txt', 'r')
mytank = pickle.load(f)
