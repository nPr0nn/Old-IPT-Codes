# Physics model for the forces and torques on a disc.

from dataclasses import dataclass
import numpy as np

@dataclass
class Environment_Variables:
    air_density = 1.225;  # kg/m^3
    g           = 9.81;   # m/s^2

    @property
    def grav_unit_vector(self):
        return np.array([0, 0, -1]);

@dataclass
class Coeff_Model:

     # Lift Coefficients
     C_l0    = 0.35;
     C_la    = 1.95;

     # Drag Coefficients
     C_d0    = 0.18;
     C_da    = 0.69;

     # Torques Coefficients
     C_xwx   = -0.013;
     C_xwz   = -0.0017;
     C_ywy   = -0.082;
     C_zwz   =  0.53;
     C_y0    = -0.014;
     C_ya    = -0.000034;

     alpha_0 = 4*(np.pi/180);

     def __init__(self, forces_coeff=None, alpha_0=None):
          if(forces_coeff != None and alpha_0 != None):
               self.C_l0 = forces_coeff[0]
               self.C_la = forces_coeff[1]
               self.C_d0 = forces_coeff[2]
               self.C_da = forces_coeff[3]
               self.alpha_0 = alpha_0
     # Angle 

     def C_lift(self, alpha):
          return self.C_l0 + self.C_la * alpha;

     def C_drag(self, alpha):
          return self.C_d0 + self.C_da * (alpha - self.alpha_0)**2;

     def C_x(self, wx, wz):
          return self.C_xwx * wx + self.C_xwz * wz;

     def C_y(self, alpha, wy):
          return self.C_y0 + self.C_ywy * wy + self.C_ya * alpha;

     def C_z(self, wz):
          return self.C_zwz * wz;
