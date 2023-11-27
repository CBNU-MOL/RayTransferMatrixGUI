import numpy as np

class rvec:
    def __init__(self, x, a, z=0):
        self.x = x
        self.a = a
        self.vec = np.array([x,a])
        self.z = z

    def propagate(self, d):
        RTM = np.array([[1,d],[0,1]])
        vec = RTM@self.vec
        return rvec(vec[0], vec[1], self.z+d)

    def thick_lens(self, n1, n2, R1, R2, t):
        RTM1 = np.array([[1,0],[(n2-n1)/R2/n1,n2/n1]])
        RTM2 = np.array([[1,t],[0,1]])
        RTM3 = np.array([[1,0],[(n1-n2)/R1/n2,n1/n2]])
        vec = RTM1@(RTM2@(RTM3@self.vec))
        return rvec(vec[0], vec[1], self.z+t)
    
    def thin_lens(self, f):
        RTM = np.array([[1,0],[-1/f,1]])
        vec = RTM@self.vec
        return rvec(vec[0], vec[1], self.z)