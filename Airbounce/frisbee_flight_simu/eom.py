from numbers import Number
from typing import Dict, Union

import numpy as np
import math

from frisbee_flight_simu.physics_model import Environment_Variables
from frisbee_flight_simu.physics_model import Coeff_Model


class EOM:
     def __init__(self, area, I_xx, I_zz, mass, environment = Environment_Variables(), model = Coeff_Model()):
          self.area        = area;
          self.diameter    = 2*np.sqrt(self.area/np.pi);
          self.I_xx        = I_xx;
          self.I_zz        = I_zz;
          self.mass        = mass;
          self.environment = environment;
          self.model       = model;

          # Pre-compute some values to optimize the ODEs
          self.force_per_v2  = 0.5 * self.environment.air_density * self.area;
          self.torque_per_v2 = self.force_per_v2 * self.diameter;  # N * m / (m/s)^2
          self.F_grav        = self.mass * self.environment.g * self.environment.grav_unit_vector;
          self.z_hat = np.array([0, 0, 1]);

     @classmethod
     def rotation_matrix_from_phi_theta(cls, phi, theta):
          sp, cp = np.sin(phi), np.cos(phi);
          st, ct = np.sin(theta), np.cos(theta);
          return cls.rotation_matrix(sp, cp, st, ct);

     @staticmethod
     def rotation_matrix(sp, cp, st, ct):
          # Compute the (partial) rotation matrix that transforms from the lab frame to the disc frame.
          return np.array([[ct, sp * st, -st * cp], [0, cp, sp], [st, -sp * ct, cp * ct]]);

     @classmethod
     def compute_angle_of_attack(cls, phi, theta, velocity: np.ndarray, return_all_variables = False):
          # Rotation matrix
          sp, cp = np.sin(phi), np.cos(phi);
          st, ct = np.sin(theta), np.cos(theta);
          rotation_matrix = cls.rotation_matrix(sp, cp, st, ct);

          # Unit vectors
          zhat = rotation_matrix[2];
          v_dot_zhat = velocity @ zhat;
          v_in_plane = velocity - zhat * v_dot_zhat;
          angle_of_attack = -np.arctan(v_dot_zhat / np.linalg.norm(v_in_plane));

          if return_all_variables:
               return angle_of_attack, sp, cp, st, ct, rotation_matrix, v_dot_zhat, v_in_plane;
          else:
               return angle_of_attack;

     def geometric_quantities(self, phi, theta, velocity: np.ndarray, angular_velocity: np.ndarray):
         angle_of_attack,_,_,st,ct,rotation_matrix,_,v_in_plane=self.compute_angle_of_attack(phi,theta,velocity,return_all_variables=True);

         zhat = rotation_matrix[2];
         xhat = v_in_plane / np.linalg.norm(v_in_plane);
         yhat = np.cross(zhat, xhat);

         # Angle of attack
         # Disc angular velocities
         angular_velocity = angular_velocity;
         w_prime = np.array([angular_velocity[0] * ct, angular_velocity[1], angular_velocity[0] * st + angular_velocity[2]]);

         # Angular velocity in lab coordinates
         w_lab = w_prime @ rotation_matrix;

         # Angular velocity components along the unit vectors in the lab frame
         w = np.array([xhat, yhat, zhat]) @ w_lab;

         return {
              "unit_vectors": {"xhat": xhat, "yhat": yhat, "zhat": zhat},
              "angle_of_attack": angle_of_attack,
              "rotation_matrix": rotation_matrix,
              "w_prime": w_prime,
              "w_lab": w_lab,
              "w": w,
         }

     def modulo(self, force):
          return math.sqrt(force[0]*force[0] + force[1]*force[1] + force[2]*force[2] )

     def compute_forces(self, phi, theta, velocity: np.ndarray, ang_velocity: np.ndarray):
          # Compute the lift, drag, and gravitational forces on the disc.
          res = self.geometric_quantities(phi, theta, velocity, ang_velocity);
          aoa = res["angle_of_attack"];
          vhat = velocity / np.linalg.norm(velocity);
          force_amplitude = self.force_per_v2 * (velocity @ velocity)

          # Compute the lift and drag forces
          res["F_lift"] = self.model.C_lift(aoa)*force_amplitude*np.cross(vhat, res["unit_vectors"]["yhat"]);
          res["F_drag"] = self.model.C_drag(aoa) * force_amplitude * (-vhat);

          # Compute gravitational force
          res["F_grav"] = self.F_grav;
          # print( res["F_lift"][2] )
          # print( str(self.modulo(res["F_drag"])) + " ; " + str(self.modulo(res["F_lift"] + res["F_grav"])) + " ; " + str(self.modulo(res["F_lift"])) + " ; " + str(self.modulo(res["F_grav"])) )
          res["F_total"] = res["F_lift"] + res["F_drag"] + res["F_grav"];
          res["Acc"] = res["F_total"] / self.mass;

          return res

     def compute_torques(self,velocity: np.ndarray, res):
          aoa = res["angle_of_attack"];
          res["torque_amplitude"] = self.torque_per_v2 * (velocity @ velocity);
          wx, wy, wz = res["w"];

          # Compute component torques (Lab Frame)
          res["T_x_lab"] = self.model.C_x(wx, wz)* res["torque_amplitude"]*res["unit_vectors"]["xhat"];
          res["T_y_lab"] = self.model.C_y(aoa, wy)* res["torque_amplitude"]*res["unit_vectors"]["yhat"];

          # Computed in the disc frame
          res["T_z"] = self.model.C_z(wz) * res["torque_amplitude"] * self.z_hat;

          # Rotate into the disc frame
          res["T_x"] = res["rotation_matrix"] @ res["T_x_lab"];
          res["T_y"] = res["rotation_matrix"] @ res["T_y_lab"];
          res["T"] = res["T_x"] + res["T_y"] + res["T_z"];
          return res;

     def compute_derivatives(self, time, coordinates: np.ndarray):
          # If the disk hit the ground, then stop calculations
          if coordinates[2] <= 0:
               return coordinates * 0;

          velocity     = coordinates[3:6];
          ang_velocity = coordinates[9:12];
          result       = self.compute_forces(coordinates[6], coordinates[7], velocity, ang_velocity);
          result       = self.compute_torques(velocity, result);

          return np.concatenate((velocity, result["Acc"], ang_velocity, result["T"]));
