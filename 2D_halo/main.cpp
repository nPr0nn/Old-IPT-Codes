#include "raylib.h"
#include "raymath.h"
#include <vector>
#include <random>
#include <iostream>
#include <cstring>
#include <algorithm>

#define SCRATCH_COLOR       (Color){40, 40, 40, 50}
#define SHINY_SCRATCH_COLOR (Color){253, 49, 30, 255}
#define LIGHT_COLOR         (Color){253, 49, 30, 255}
#define SCRATCH_THICKNESS 1

typedef struct Scratch{
     Vector2 p1;
     Vector2 p2;
} Scratch;

float random_float(float min, float max){
     std::random_device rd; 
     std::mt19937 engine(rd());
     std::uniform_real_distribution<> dist(min, max);
     return dist(engine);
}

Vector2 interp(float t, Vector2 p, Vector2 a, Vector2 b){
     Vector2 f;
     f.x = (1 - t) * a.x  +  t * b.x - p.x;
     f.y = (1 - t) * a.y  +  t * b.y - p.y;

     return f;
}

float norm_square(Vector2 a){
     return ( a.x * a.x + a.y * a.y);
}

float norm(Vector2 a){
     return sqrt(norm_square(a));
}

Vector2 point_on_scratch_closest_to(Scratch s, Vector2 p){
     Vector2 v = {s.p2.x - s.p1.x, s.p2.y - s.p1.y};
     Vector2 u = {s.p1.x - p.x, s.p1.y - p.y};
     
     float vu  = v.x * u.x + v.y * u.y;
     float vv  = v.x * v.x + v.y * v.y;

     float t   = (-vu)/(vv);

     if(t >= 0 && t <= 1) return interp(t, {0, 0}, s.p1, s.p2);

     float g0 = norm_square(interp(0, p, s.p1, s.p2));
     float g1 = norm_square(interp(1, p, s.p1, s.p2));

     if(g0 <= g1) return s.p1;

     return s.p2;
}


Vector2 addV(Vector2 a, Vector2 b){
     Vector2 c = {a.x + b.x, a.y + b.y};
     return c;
}

Vector2 negV(Vector2 a){
     Vector2 r = {-a.x, -a.y};
     return r;
}

float dot_product(Vector2 a, Vector2 b){
     return (a.x * b.x + a.y * b.y);
}

float angle_between_vectors(Vector2 origin, Vector2 a, Vector2 b){
     a = addV(a, negV(origin));
     b = addV(b, negV(origin));
     float cosine = dot_product(a, b)/(norm(a) * norm(b));
     return acos(cosine);
}

float distance(Vector2 a, Vector2 b){
     float d = sqrt( (a.x - b.x)*(a.x - b.x) + (a.y - b.y)*(a.y - b.y) );
     return d;
}

// ------------------------------------------------------------------------

Scratch new_random_scratch(float window_width, float window_height){
     Scratch scratch;
     float percentage = 0.3;

     scratch.p1 = (Vector2) {random_float(0, window_width), random_float(0, window_height)};    
     float length = (percentage*window_width)*(std::abs(random_float(-1, 1)));
     float angle  = random_float(0, 2*PI);
     
     float bias   = random_float(0, 1);
    
     //if(bias < 0.4 && bias > 0.2){
          //angle = DEG2RAD * (-30);
     //}
     //if(bias < 0.2) angle = DEG2RAD * (55);

     scratch.p2 = (Vector2) { (float)(scratch.p1.x + length*cos(angle)), 
                              (float)(scratch.p1.y + length*sin(angle)) }; 

     return scratch;
}

void draw_light(Vector2 light, Vector2 observer, float radius){
     DrawCircleV(addV(light, observer), radius, LIGHT_COLOR);
     return;
}

void draw_scratch(Scratch scratch, Vector2 observer){
     DrawLineEx(addV(scratch.p1, observer), addV(scratch.p2, observer), SCRATCH_THICKNESS, SCRATCH_COLOR);
     return;
}

void draw_reflection(Scratch scratch, Vector2 light, Vector2 observer, float light_radius){
 
     Vector2 scratch_point_closest = point_on_scratch_closest_to(scratch, light);    
     //DrawLineV(addV(light, observer), addV(scratch_point_closest, observer), RED);

     float angle_between = 0;

     if(scratch_point_closest.x == scratch.p1.x && scratch_point_closest.y == scratch.p1.y){
          angle_between = angle_between_vectors(scratch_point_closest, scratch.p2, light);
     }
     else{
          angle_between = angle_between_vectors(scratch_point_closest, scratch.p1, light);
     }

     std::cout << angle_between << std::endl;

     float radius = 240;
     if( (distance(scratch.p1, light) <= radius) && (distance(scratch.p2, light) <= radius )){

          if(angle_between - PI/2 < 0.001){
               Vector2 shiny_scratch_middle = scratch_point_closest;

               float k1 = light_radius/norm(addV(scratch.p1, negV(shiny_scratch_middle)));
               float k2 = light_radius/norm(addV(scratch.p2, negV(shiny_scratch_middle)));

               Vector2 shiny_scratch_end1 = interp(k1, {0, 0}, shiny_scratch_middle, scratch.p1);
               Vector2 shiny_scratch_end2 = interp(k2, {0, 0}, shiny_scratch_middle, scratch.p2);

               //DrawCircleV(shiny_scratch_middle, 5, WHITE);
               DrawLineEx(addV(shiny_scratch_middle, observer), addV(shiny_scratch_end1, observer), SCRATCH_THICKNESS, SHINY_SCRATCH_COLOR);
     float theta = PI/2;
               DrawLineEx(addV(shiny_scratch_middle, observer), addV(shiny_scratch_end2, observer), SCRATCH_THICKNESS, SHINY_SCRATCH_COLOR);
          }

     }
     return;
}

// ------------------------------------------------------------------------

int main(void){
     int window_width  = 640; 
     int window_height = 640;
     InitWindow(window_width, window_height, "2D Scratches");
     
     // Observer
     Vector2 observer = {0, 0};
     float speed      = 0.1;

     // Light source
     Vector2 light      = {(float)window_width/2, (float)window_height/2};
     float light_radius = 20;

     // Scratches
     int number_of_scratches = 420;
     std::vector <Scratch> scratches; 
     for(int i = 0; i < number_of_scratches; i++){
          scratches.push_back(new_random_scratch((float)window_width,(float)window_height));
     }


     int frame_counter = 0;
     while (!WindowShouldClose()){
          ClearBackground(BLANK);
          BeginDrawing();
 
          if(IsKeyDown(KEY_Z)) light_radius += 0.1;
          if(IsKeyDown(KEY_X)) light_radius -= 0.1;

          if(IsKeyDown(KEY_W)) observer.y += speed;
          if(IsKeyDown(KEY_A)) observer.x += speed;
          if(IsKeyDown(KEY_S)) observer.y -= speed;
          if(IsKeyDown(KEY_D)) observer.x -= speed;

          if(IsMouseButtonDown(0)) light = addV(GetMousePosition(), negV(observer));
          draw_light(light, observer, light_radius);

          for(int i = 0; i < number_of_scratches; i++){
               draw_scratch(scratches[i], observer);
               draw_reflection(scratches[i], light, observer, light_radius);
          }


          frame_counter += 1;
          EndDrawing();
          
          const char *file_path = "animation_frames/screen_";
          const char *file_extension = ".png";

          char file_index[256];
          sprintf(file_index, "%04d", frame_counter);

          char file_name[100];
          strcpy(file_name, file_path);
          strcat(file_name, file_index);
          strcat(file_name, file_extension);

          TakeScreenshot("halo2.png");
          //TakeScreenshot(file_name);
     }

     CloseWindow();
     return -1;
}
