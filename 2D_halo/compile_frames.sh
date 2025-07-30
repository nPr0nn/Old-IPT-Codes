#!/bin/bash
cd animation_frames
#ffmpeg -framerate 60 -i screen_%04d.png -lavfi split[v],palettegen,[v]paletteuse sparks.gif
#ffmpeg -f image2 -framerate 60 -i screen_%04d.png sparks.mp4
ffmpeg -f image2 -framerate 30 -i screen_%04d.png halo_animation_GIF.gif
mv halo_animation_GIF.gif ../
rm *.png

