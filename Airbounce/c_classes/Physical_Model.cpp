#include "../c_headers/Physical_Model.h"
#include <math.h>

Physical_Model::Physical_Model(){
     // Lift Coefficients
     C_l0    = 0.33;
     C_la    = 1.90;

     // Drag Coefficients
     C_d0    = 0.18;
     C_da    = 0.69;

     // Torques Coefficients
     C_xwx   = -0.013;
     C_xwz   = -0.0017;
     C_ywy   = -0.082; 
     C_zwz   =  0.43;
     C_y0    = -0.014;
     C_ya    = -0.000034;

     // Angle 
     alpha_0 = 4*(M_PI/180);
}

float Physical_Model::C_lift(float alpha){
     return C_l0 + (C_la * alpha);
}
float Physical_Model::C_drag(float alpha){
     return C_d0 + C_da * (alpha - alpha_0)*(alpha - alpha_0);
}
float Physical_Model::CT_x(float wx, float wz){
     return (C_xwx * wx) + (C_xwz * wz );
}
float Physical_Model::CT_y(float alpha, float wy){
     return C_y0 + (C_ywy * wy) + (C_ya * alpha);
}
float Physical_Model::CT_z(float wz){
     return C_xwz * wz;
}
