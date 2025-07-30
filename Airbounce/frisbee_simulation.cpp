#include "raylib.h"
#include "raymath.h"

#include "c_headers/CSVReader.h"
#include "c_headers/Disc.h"
#include "c_classes/Disc.cpp"

#include <vector>
#include <string>
#include <algorithm>
#include <math.h>

Vector3 neg(Vector3 v){
     Vector3 neg_v = {-v.x, -v.y, -v.z};
     return neg_v;
}

int main(){
     // Window Initialization
     //--------------------------------------------------------------------------------------
     const int screenWidth  = 1280;
     const int screenHeight = 720;
     const float pi = M_PI;

     InitWindow(screenWidth, screenHeight, "Frisbee Flight Simulation - Airbounce");

     // Define the camera to look into 3d space
     Camera3D camera = { 0 };
     camera.position = (Vector3){ 2.0f, 2.0f, 2.0f };    // Camera position
     camera.target = (Vector3){ 0.0f, 0.0f, 0.0f };      // Camera looking at point
     camera.up = (Vector3){ 0.0f, 1.0f, 0.0f };          // Camera up vector (rotation towards target)
     camera.fovy = 75.0f;                                // Camera field-of-view Y
     camera.projection = CAMERA_PERSPECTIVE;             // Camera mode type
     //SetCameraMode(camera, CAMERA_FREE);                 // Set a free camera mode
     SetTargetFPS(60);                                   // Set simulation to run at 60 frames-per-second

     // Define Axis
     Vector3 x_axis                      = { 1.0f, 0.0f, 0.0f };
     Vector3 y_axis                      = { 0.0f, 1.0f, 0.0f };
     Vector3 z_axis                      = { 0.0f, 0.0f, 1.0f };

     Vector3 vnull                       = { 0.0f, 0.0f, 0.0f };
     //--------------------------------------------------------------------------------------

     std::string file_name = "simu_data.csv";
     std::vector<std::vector<float>> sd = CSVRead(file_name); // simulation data
     int number_of_data_point = sd.size();

     Vector3 initial_position            = { sd[0][1], sd[0][0], sd[0][2] };
     Vector3 initial_angles              = { sd[0][3], -sd[0][4], sd[0][5] };

     Disc frisbee = Disc(initial_position, vnull, initial_angles, vnull);
     
     // Simulation Animation
     int startSimulation = 0;
     int frameCount = 0;
     while (!WindowShouldClose()){
          //----------------------------------------------------------------------------------
          UpdateCamera(&camera);        
          if (IsKeyDown('Z')) camera.target = (Vector3){ 0.0f, 0.0f, 0.0f };
          
          if (IsKeyDown('A')) camera.position = (Vector3){ frisbee.get_x() + 5, frisbee.get_z(), frisbee.get_y() };
          if (IsKeyDown('S')) camera.position = (Vector3){ frisbee.get_x(), frisbee.get_z(), frisbee.get_y() + 5 };
          if (IsKeyDown('D')) camera.position = (Vector3){ frisbee.get_x(), frisbee.get_z() + 3, frisbee.get_y() - 1};
          
          if (IsKeyDown('R')){
               frameCount = 0;
               startSimulation = 0;
               frisbee.set_positions(sd[frameCount][1], sd[frameCount][0], sd[frameCount][2]);
               frisbee.set_angles(sd[frameCount][3], -sd[frameCount][4], 0);
          }
          //----------------------------------------------------------------------------------
          
          //printf("%f %f %f \n", camera.position.x, camera.position.z, camera.position.y);
          ClearBackground(BLACK);

          BeginDrawing();
          BeginMode3D(camera);

          DrawGrid(100, 1.0f);
          DrawLine3D(neg(x_axis), x_axis, RED); 
          DrawLine3D(neg(y_axis), y_axis, BLUE); 
          DrawLine3D(neg(z_axis), z_axis, GREEN); 

          if (IsKeyDown(KEY_SPACE)) startSimulation = 1;
          if(startSimulation == 1 and frameCount < number_of_data_point){
               frisbee.set_positions(sd[frameCount][1], sd[frameCount][0], sd[frameCount][2]);
               //frisbee.set_angles(sd[frameCount][3], -sd[frameCount][4], 0);
               frisbee.set_angles(sd[frameCount][3], -sd[frameCount][4], sd[frameCount][5]);

               //for (int i = 0; i <= 6; i++) printf("%lf , ", sd[frameCount][i]);
               //printf("\n");

               frameCount += 1;
               camera.target = (Vector3){ frisbee.get_x(), float(frisbee.get_z() - 1.2), frisbee.get_y()};

               const char *file_path      = "animation_frames/screen_";
               const char *file_extension = ".png";

               char file_index[256]; 
               sprintf(file_index, "%04d", frameCount);

               char file_name[100]; 
               strcpy(file_name, file_path);
               strcat(file_name, file_index);
               strcat(file_name, file_extension);

               printf("%s \n", file_name);
               //TakeScreenshot(file_name);
          }

          for(int i = 0; i < frameCount; i++) DrawSphere( {sd[i][1], sd[i][2], sd[i][0]}, 0.01, YELLOW);
          frisbee.draw();
         
          EndMode3D();         
          EndDrawing();


     }

     // De-Initialization
     //--------------------------------------------------------------------------------------
     CloseWindow();        // Close window and OpenGL context
     //--------------------------------------------------------------------------------------
}
