#include "../c_headers/Disc.h"

#include <boost/numeric/odeint.hpp>
#include "raylib.h"
#include "raymath.h"
#include <math.h>

Disc::Disc(Vector3 position, Vector3 velocity, Vector3 rotation_angle, Vector3 angular_velocity){
     Frisbee_CAD = LoadModel("3D_Model/Frisbee.obj");
     self_physical_model = Physical_Model();

     // Environment variables
     pi            = M_PI;
     rho_air       = 1.225;
     g             = 9.78;

     // Positions (m)
     self_x        = position.x;
     self_y        = position.y;
     self_z        = position.z;

     // Velocities (m/s)
     self_vx       = velocity.x;
     self_vy       = velocity.y;
     self_vz       = velocity.z;

     // Angles of Rotation (Euler) (radians)
     self_phi      = rotation_angle.x;
     self_theta    = rotation_angle.y;
     self_gamma    = rotation_angle.z;

     // Angular Velocities
     self_dphi     = angular_velocity.x;
     self_dtheta   = angular_velocity.y;
     self_dgamma   = angular_velocity.z;

     // Physical attributes
     self_mass     = 0.125; // kg
     self_diameter = 0.23;  // m
     self_area     = pi*((self_diameter*self_diameter)/4);
     self_Ixx      = 0.001219;
     self_Iyy      = self_Ixx;
     self_Izz      = 0.002352;
}

void Disc::draw(){
     //Frisbee_CAD.transform = MatrixRotateXYZ((Vector3){self_theta, 0, self_phi});
     Frisbee_CAD.transform = MatrixRotateXYZ((Vector3){ 0, self_gamma, 0});
     Frisbee_CAD.transform = MatrixMultiply(Frisbee_CAD.transform, MatrixRotateXYZ((Vector3){ self_theta, 0, self_phi}));

     Vector3 position = {self_x, self_z, self_y};
     //Color color = (Color){ 255, 66, 5, 255};
     //Color wire_color = (Color){ 176, 56, 9, 255 };

     Color color = (Color){ 78, 45, 129, 255};
     Color wire_color = (Color){ 57, 37, 100, 255 };

     DrawModel(Frisbee_CAD, position, 3.0f, color);
     DrawModelWires(Frisbee_CAD, position, 3.0f, wire_color);
}
