import math
import numpy as np


class Transform:
    def __init__(self):
        self.MVM = np.identity(4)

    def get_MVM(self):
        return self.MVM

