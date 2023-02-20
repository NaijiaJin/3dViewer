import math
import numpy as np
from Transform import *

class Camera:
    def __init__(self, fov, aspect, near, far):
        f = 1/math.tan(math.radians(fov/2))
        a = f/aspect
        b = f
        c = (far + near) /(near - far)
        d = 2* near *far/(near - far)
        self.PPM  = np.matrix([[a, 0,0,0],[0,b,b,0],[0,0,c,d],[0,0,-1,0]])
        self.VM = np.identity(4)
        self.transform = Transform()
        self.transform.MVM = np.matrix([[1,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,1]])


    def get_PPM(self):
        return self.PPM

    def get_VM(self):
        return self.transform.MVM
