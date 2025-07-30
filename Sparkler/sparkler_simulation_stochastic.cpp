#include "raylib.h"

#include "SparkClass.h"
#include "SparkClass.cpp"

#include <cstring>
#include <chrono>
#include <cstdio>
#include <algorithm>
#include <vector>
#include <random>
#include <math.h>

float gaussian_distribution(double min, double max){
     unsigned seed = static_cast<int>(std::chrono::system_clock::now().time_since_epoch().count());
     std::default_random_engine gaussian_generator(seed);
     float mid = (min+max)/2;
     std::normal_distribution<double>distribution(mid, mid/3);
     float number = (float) std::clamp(distribution(gaussian_generator), min, max);
     return number;
}

float uniform_distribution(double min, double max){
     unsigned seed = static_cast<int>(std::chrono::system_clock::now().time_since_epoch().count());
     std::mt19937 uniform_generator(seed);
     std::uniform_real_distribution <double> distribution(min, max);
     float number = (float) distribution(uniform_generator);
     return number;
}

float exp_distribution(double gamma){
     unsigned seed = static_cast<int>(std::chrono::system_clock::now().time_since_epoch().count());
     std::default_random_engine exp_generator(seed);
     std::exponential_distribution<double> distribution(gamma);
     float number = (float) distribution(exp_generator);
     return number;
}

float max(float a, float b){
     if(a > b) return a;
     return b;
}

int main(){
     // Initialization
     //--------------------------------------------------------------------------------------
     const int screenWidth  = 1280;
     const int screenHeight = 720;

     InitWindow(screenWidth, screenHeight, "Sparkler Simulation - Stochastic Process");

     // Define the camera to look into 3d space
     Camera3D camera = { 0 };
     camera.position = (Vector3){ 0.0f, 0.0f, 10.0f }; // Camera position

     camera.target = (Vector3){ 0.0f, 5.0f, 0.0f };      // Camera looking at point
     camera.up = (Vector3){ 0.0f, 1.0f, 0.0f };          // Camera up vector (rotation towards target)
     camera.fovy = 55.0f;                                // Camera field-of-view Y
     camera.projection = CAMERA_PERSPECTIVE;             // Camera mode type
     SetCameraMode(camera, CAMERA_FREE);                 // Set a free camera mode
     SetTargetFPS(60);                                   // Set simulation to run at 60 frames-per-second

     Vector3 origin = { 0.0f, 0.0f, 0.0f };

     // Setup Variables
     float heights[4]            = {0, 0.16, 0.0725, 0.0725};     // ground, candle, sparkler rod, sparkler binder
     float candle_radius         = 0.005f;                        // just for visualization
     Color candle_color          = (Color){ 163, 163, 163, 255 };
     Color wires_candle_color    = (Color){ 123, 123, 123, 255 };
     Color sparkler_rod_color    = (Color){ 199, 104,  48, 255 };
     Color sparkler_binder_color = (Color){  82,  82,  82, 255 };
     Color spark_color           = (Color){ 255, 157, 71, 255 };
     Color spark_outline_color   = (Color){ 255,  94, 64, 255 };
     Color colors[4]             = {RED, RED, sparkler_rod_color, sparkler_binder_color};
     float pmr                   = 20;  // Pixel-meter ratio

     // Sparkler Variables
     float time_to_burn          = 28;                               // seconds (s)
     float dt                    = 0.0001;
     float time                  = 0;
     float combustible_lenght    = heights[3];                       // meter (m)
     float sparkler_tip_height   = 0.305;                            // meter (m)
     float burning_velocity      = combustible_lenght/time_to_burn;  // meter/second (m/s)
     float pi                    = 3.141592653;

     // Stochastic Process Randomness

     // Sparks Vector
     std::vector <Spark> sparks;
     float time_launch = 0;

     //--------------------------------------------------------------------------------------
     float  flame_average_distance = 0;
     float  flame_size             = 0;
     float  flame_max_distance     = 0;
     int frame_counter = 0;
     while (time < time_to_burn and !WindowShouldClose()){
          // Update Simulation Clock
          time += dt;
          time_launch += dt;
          //----------------------------------------------------------------------------------
          UpdateCamera(&camera);        
          if (IsKeyDown('Z')) camera.target = (Vector3){ 0.0f, 0.0f, 0.0f };
          //----------------------------------------------------------------------------------

          // Draw
          //----------------------------------------------------------------------------------
          ClearBackground(BLACK);

          BeginDrawing();
          BeginMode3D(camera);
               float sparkler_burning_height = sparkler_tip_height - time*burning_velocity;
               sparkler_burning_height = sparkler_tip_height;

               Vector3 candle_point_end  = {0.0f, (float)(pmr*(heights[1])), 0.0f };
               Vector3 burning_point     = {0.0f, (float)(pmr*sparkler_burning_height), 0.0f };
               Vector3 burning_point_end = {0.0f, (float)(pmr*(heights[1]+heights[2])), 0.0f };
               DrawCylinder(origin, pmr*candle_radius, pmr*candle_radius, pmr*heights[1], 200, candle_color);
               DrawCylinderWires(origin, pmr*candle_radius, pmr*candle_radius, pmr*heights[1], 200, wires_candle_color);
               DrawLine3D(candle_point_end, burning_point_end, colors[2]);
               DrawLine3D(burning_point_end, burning_point, colors[3]);
               DrawSphere( burning_point, 0.03, RED);

               //camera.target = burning_point;      // Camera looking at point

               printf("%f %f %f \n", camera.position.x, camera.position.y, camera.position.z);
               printf("%f %f %f \n", camera.position.x, camera.position.y, camera.position.z);

               float temperature = gaussian_distribution(1381, 1391);
               float v_0         = gaussian_distribution(5.21, 8.36);
               float radius      = gaussian_distribution(0.03, 0.08);
               float phi         = acos(1 - 2*uniform_distribution(0, 1));
               float theta       = 2*pi*uniform_distribution(0, 1); 

               float explosion_discriminant = uniform_distribution(0, 1);
               
               temperature = 1391;
               v_0         = 8.36;
               radius      = 0.08;
               phi         = pi/2;
               theta       = 0;
               explosion_discriminant = 0;

               Spark spark = Spark(0, 0, sparkler_burning_height, temperature, radius, theta, phi, v_0, 78, explosion_discriminant, 0);
               float time_of_explosion = gaussian_distribution(0, spark.get_life_time());
               spark.set_time_of_explosion(time_of_explosion);

               //printf("%f %f \n", uniform_distribution(0, 1), uniform_distribution(0, 1));
               if(IsKeyPressed('S') ) sparks.push_back(spark);              
               double average_distance = 0;
               int sparks_alive = 0;
               for(int i = 0; i < sparks.size(); i++){
                    if(sparks[i].get_current_temperature() > sparks[i].get_draper_temperature()){
                         Vector3 spark_position = {pmr*sparks[i].get_x(), pmr*sparks[i].get_z(), pmr*sparks[i].get_y()};
                         Vector3 spark_origin_position = {pmr*sparks[i].get_x_0(), pmr*sparks[i].get_z_0(), pmr*sparks[i].get_y_0()};

                         //printf("%f %f %f \n", spark_position.x, spark_position.y, spark_position.z);
                         
                         if(sparks[i].will_explode()){
                              if(sparks[i].exploded()){
                                   DrawSphere( spark_position, sparks[i].get_current_radius(), RED);
                                   // Branching
                                   int number_of_branchings = (int) uniform_distribution(4, 14);
                                   number_of_branchings = 1;
                                   for(int j = 0; j < number_of_branchings; j++){
                                        float child_temperature = sparks[i].get_current_temperature();
                                        float child_v_0         = sparks[i].get_current_velocity() + sparks[i].get_current_velocity()/number_of_branchings;
                                        float child_radius      = gaussian_distribution(0.02, sparks[i].get_current_radius());
                                        float child_phi         = acos(1 - 2*uniform_distribution(0, 1));
                                        float child_theta       = 2*pi*uniform_distribution(0, 1); 
                                        float child_explosion_discriminant = uniform_distribution(0, 1);

                                        child_temperature = 1391;
                                        child_v_0         = 8.36 + 8.36/4;

                                        child_phi         = pi/2;
                                        child_theta       = 0;
                                        child_explosion_discriminant = 0;

                                        Spark child_spark = Spark(sparks[i].get_x(), sparks[i].get_y(), sparks[i].get_z(), 
                                                  child_temperature, child_radius, child_theta, child_phi, child_v_0, 78, 
                                                  child_explosion_discriminant, sparks[i].get_depth() + 1);
                                        
                                        float child_time_of_explosion = gaussian_distribution(0, child_spark.get_life_time());

                                        child_spark.set_time_of_explosion(child_time_of_explosion);
                                        sparks.push_back(child_spark);
                                   }
                              }
                              else DrawSphere( spark_position, sparks[i].get_current_radius(), spark_outline_color);
                         }
                         else DrawSphere( spark_position, sparks[i].get_current_radius(), spark_color);
                         
                         if(sparks[i].get_depth() == 0) DrawLine3D(spark_origin_position, spark_position, YELLOW);
                         else if (sparks[i].get_depth() == 1) DrawLine3D(spark_origin_position, spark_position, ORANGE);
                         else DrawLine3D(spark_origin_position, spark_position, RED);

                         double xx = sparks[i].get_x();
                         double yy = sparks[i].get_y();
                         average_distance += sqrt(xx*xx + yy*yy);
                         sparks_alive += 1;
                         sparks[i].move(dt);
                    }
               }
               Color average_sphere_color = (Color){245, 161, 66, 50};
               Color average_sphere_wire_color = (Color){184, 122, 51, 80};

               average_distance /= sparks_alive;
               //DrawSphere(burning_point, pmr*average_distance, average_sphere_color);
               //DrawSphereWires(burning_point, pmr*average_distance, 2, 2, average_sphere_wire_color);

               //printf("%f \n", average_distance);
               flame_max_distance = max(average_distance, flame_max_distance);
               flame_average_distance += average_distance;
               frame_counter += 1;
               DrawGrid(10, 1.0f);
          EndMode3D();         
          EndDrawing();
          
          const char *file_path      = "animation_frames/screen_";
          const char *file_extension = ".png";

          char file_index[256]; 
          sprintf(file_index, "%04d", frame_counter);

          char file_name[100]; 
          strcpy(file_name, file_path);
          strcat(file_name, file_index);
          strcat(file_name, file_extension);

          //printf("%s \n", file_name);
          //TakeScreenshot(file_name);
          //----------------------------------------------------------------------------------
     }
     frame_counter = (float) frame_counter;
     flame_average_distance /= frame_counter;
     flame_size = (4/3)*pi*(flame_average_distance)*(flame_average_distance)*(flame_average_distance);
     printf("\n\n\n Flame Maximum Distance: %f \n", flame_max_distance);
     printf("Flame Average Distance: %f \n", flame_average_distance);
     printf("Flame Size: %f \n\n\n", flame_size);

     // De-Initialization
     //--------------------------------------------------------------------------------------
     CloseWindow();        // Close window and OpenGL context
     //--------------------------------------------------------------------------------------

     return 0;
}
