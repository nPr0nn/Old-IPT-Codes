#include "SparkClass.h"
#include <math.h>
#include <random>

float pow(float a, int b) {
    if (b == 0) return 1;
    float res = pow(a, b / 2);
    if (b % 2) return res * res * a;
    else return res * res;
}

float convert_angle(float angle_degrees){
     float pi = 3.14159;
     float angle_radians = (angle_degrees/180)*pi;
     return angle_radians;
}

Spark::Spark(float x_0, float y_0, float z_0, float T_0, float radius, float theta, float phi, 
             float v0, float gamma, float explosion_discrimant, float depth){
     // Eviroment Variables
     self_T_air                          = 28.0;    // Air Temperature                        - [K] 
     pi                                  = 3.141592653;
     g                                   = 9.798;   // Gravity                                - [m/s²] 

     // Spark Nature Variables
     self_radius                         = radius;  // Spark Radius                           - [m]
     self_T_0                            = T_0;
     self_T_current                      = T_0;
     self_T_draper                       = 798;     // Incandescence Temperature              - [K]
     self_rho_iron_oxide                 = 5.170;   // Iron Oxide (Fe3O4) Density             - [g/cm³]
     self_specific_heat_iron_oxide       = 0.651;   // Iron Oxide (Fe3O4) Specific Heat       - [J/gK] 
     self_thermal_condutivity_iron_oxide = 0.059;   // Iron Oxide (Fe3O4) Thermal Condutivity - [J/cm s K]

     self_volume                         = (4/3)*PI*(pow(self_radius, 3));
     self_thermal_diffusivity            = self_thermal_condutivity_iron_oxide/(self_rho_iron_oxide*self_specific_heat_iron_oxide);
     self_cooling_constant               = (3*self_thermal_diffusivity)/(2*(pow(self_radius,2)));
     self_life_time                      = (log((self_T_0 - self_T_air)/(self_T_draper - self_T_air)))/(self_cooling_constant);
     self_time                           = 0;

     // Projectile Motion Variables
     self_theta                          = theta;
     self_phi                            = phi;
     self_v0                             = v0;
     self_gamma                          = gamma;
     
     // 
     self_v0x                            = self_v0*sin(self_phi)*cos(self_theta);
     self_v0y                            = self_v0*sin(self_phi)*sin(self_theta);
     self_v0z                            = self_v0*cos(self_phi);

     self_x                              = x_0;
     self_y                              = y_0;
     self_z                              = z_0;
     
     self_x_0                            = x_0;
     self_y_0                            = y_0;
     self_z_0                            = z_0;

     //
     self_explosion_discrimant           = explosion_discrimant;
     self_depth                          = depth;
     self_already_exploded               = false;
}

bool Spark::will_explode(){
     if(self_explosion_discrimant < 4*self_radius and self_depth < 2) return 1;
     else return 0;
}

bool Spark::exploded(){
     if(self_time > self_time_of_explosion and self_already_exploded == false){
          self_already_exploded = true;
          return 1;
     }
     else return 0;
}

void Spark::update_current_temperature(float time){
     self_T_current = self_T_air + (self_T_0 - self_T_air)*exp( -time*(self_cooling_constant) );
}
void Spark::update_current_radius(float radius){
     self_radius = radius;
     self_cooling_constant    = (3*self_thermal_diffusivity)/(2*(pow(self_radius,2)));
     self_life_time           = (log((self_T_0 - self_T_air)/(self_T_draper - self_T_air)))/(self_cooling_constant);
}

void Spark::branch(float branching_number){
     self_volume              = self_volume/branching_number;
     self_radius              = cbrt( (3*self_volume)/(4*pi) );
     self_cooling_constant    = (3*self_thermal_diffusivity)/(2*(pow(self_radius,2)));
     self_T_0                 = self_T_current;
     self_life_time           = (log((self_T_0 - self_T_air)/(self_T_draper - self_T_air)))/(self_cooling_constant);
}

void Spark::move(float dt){
     self_time += dt;
     update_current_temperature(self_time);
     self_x = self_x_0 + self_v0x*( (1 - exp(-self_gamma*self_time))/self_gamma );
     self_y = self_y_0 + self_v0y*( (1 - exp(-self_gamma*self_time))/self_gamma );
     self_z = self_z_0 + (self_v0z + g/self_gamma)*((1 - exp(-self_gamma*self_time))/self_gamma ) - (g*self_time)/self_gamma;
}

