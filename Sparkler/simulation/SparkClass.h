#ifndef SPARK_H
#define SPARK_H

class Spark{
     private:
          // Environment Variables
          float self_T_air;
          float pi;
          float g;

          // Spark Nature Variables
          float self_time;
          float self_radius;
          float self_volume;
          float self_T_0;
          float self_T_current;
          float self_T_draper;
          float self_rho_iron_oxide;
          float self_specific_heat_iron_oxide;
          float self_thermal_condutivity_iron_oxide;
          float self_thermal_diffusivity;
          float self_cooling_constant;
          float self_life_time;

          // Projectile Motion Variables
          float self_theta;
          float self_phi;
          float self_v0;
          float self_gamma;
          
          float self_v0x;
          float self_v0y;
          float self_v0z;

          float self_x;
          float self_y;
          float self_z;

          float self_x_0;
          float self_y_0;
          float self_z_0;

          // Explosion Variables
          float self_explosion_discrimant; 
          float self_time_of_explosion;
          bool  self_already_exploded;
          float self_depth;

     public:
          Spark(float x_0, float y_0, float z_0, float T_0, float radius, float theta, float phi, float v0, 
                float gamma, float explosion_discrimant, float depth);

          bool exploded();
          bool will_explode();

          void update_current_temperature(float time);
          void update_current_radius(float radius);
          void move(float time);
          void branch(float branching_number);

          float get_current_temperature() { return self_T_current; }
          float get_draper_temperature() { return self_T_draper; }
          float get_depth() { return self_depth; }

          float get_current_velocity() { return self_v0; }
          float get_current_radius() { return self_radius; }
          float get_current_volume() { return self_volume; }
          float get_life_time() { return self_life_time; }
          float get_time() { return self_time; }

          void set_time_of_explosion(float time_of_explosion) { self_time_of_explosion = time_of_explosion; }

          float get_x() { return self_x; }
          float get_y() { return self_y; }
          float get_z() { return self_z; }

          float get_x_0() { return self_x_0; }
          float get_y_0() { return self_y_0; }
          float get_z_0() { return self_z_0; }
};

#endif
