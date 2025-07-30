#ifndef DISC_H
#define DISC_H

#include "raylib.h"
#include "../c_headers/Physical_Model.h"
#include "../c_classes/Physical_Model.cpp"

class Disc{
     private:
          Model Frisbee_CAD;
          Physical_Model self_physical_model;

          // Environment variables
          float pi;
          float rho_air;
          float g;

          // Positions
          float self_x;
          float self_y;
          float self_z;

          // Velocities
          float self_vx;
          float self_vy;
          float self_vz;

          // Angles of Rotation (Euler)
          float self_phi;   // roll
          float self_theta; // pitch
          float self_gamma; // yaw

          // Angular Velocities
          float self_dphi;
          float self_dtheta;
          float self_dgamma;

          // Physical attributes
          float self_mass;
          float self_radius;
          float self_diameter;
          float self_area;
          float self_Ixx;
          float self_Iyy;
          float self_Izz;

     public:
          Disc(Vector3 position, Vector3 velocity, Vector3 rotation_angle, Vector3 angular_velocity);

          // Get Methods
          Physical_Model get_model(){ return self_physical_model; }
          Model get_CAD(){ return Frisbee_CAD; }
          float get_x(){ return self_x; }
          float get_y(){ return self_y; }
          float get_z(){ return self_z; }


          // Set Methods
          void set_angles(float phi, float theta, float gamma){ 
               self_theta = theta;
               self_gamma = gamma;
               self_phi   = phi;
          }

          void set_positions(float x, float y, float z){ 
               self_x     = x;
               self_y     = y;
               self_z     = z;
          }
        
          // Implemented Methods
          void draw();
};

#endif
