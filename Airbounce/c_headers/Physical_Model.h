#ifndef MODEL_H
#define MODEL_H

class Physical_Model{
     private:
          // Coefficient model for a disc. Holds all of the aerodynamic
          // parameters coupling the kinematic variables (spins and angles)
          // to the force magnitudes.
          
          // Lift Coefficients
          float C_l0;
          float C_la;

          // Drag Coefficients
          float C_d0;
          float C_da;

          // Torques Coefficients
          float C_xwx;
          float C_xwz;
          float C_ywy;
          float C_zwz;
          float C_y0;
          float C_ya;

          // Angle 
          float alpha_0;

     public:
          Physical_Model();
          float C_lift(float alpha);
          float C_drag(float alpha);
          
          float CT_x(float wx, float wz);
          float CT_y(float alpha, float wy);
          float CT_z(float wz);
};

#endif
