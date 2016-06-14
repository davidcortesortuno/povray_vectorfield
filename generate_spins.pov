#include "colors.inc"
#include "metals.inc"
#include "screen.inc"
#include "textures.inc"
global_settings { assumed_gamma 1.6 }
// background { color Black }
// We leave transparent background for now

camera {
    // The center of the skyrmion is at <20, 0, -20>
    // We transformed the coordinates to the Povray ref frame as:
    // x --> -z , y --> x, x --> y
    location <18, 9, -13>
    look_at <18, 0, -30>
    // Change the aspect ratio to 2:1
    up        1 * y
    right     2 * x
}

// Area loght is for better shadows (for a transparent background
// we don't see this effect). We could move the light further to the
// centre
light_source { <10, 15, -10> 
               color White
               area_light <0, 8, 0>, <0, 0, 8>, 5, 5
               adaptive 1
               // spotlight
               // point_at <0, 5, 5>
               // tightness 20 
               // radius 15
               // falloff 30 
             }

#declare cone_scale=0.5;
// Load the "spins" from the include file at the end:
// 3 coordinates, 3 spin directions, and rgb colour values
// from every row
#macro spins(cx, cy, cz, sx, sy, sz, rr, gg, bb)
union{
cone {<cx + 0.5 * sx * cone_scale, 
       cy + 0.5 * sy * cone_scale,
       cz + 0.5 * sz * cone_scale
       >, 
      cone_scale * 0.5,
      <cx - 0.5 * sx * cone_scale,
       cy - 0.5 * sy * cone_scale,
       cz - 0.5 * sz * cone_scale
       >,
      0.0
      // These settings will create kind of plastic cones
      texture{ 
              // Load the color giving rgb values
              pigment { color rgb < rr, gg, bb > }
              // We will make the cones to look like plastic
              finish { specular 1 roughness 0.001 
                       reflection{0 0.83 fresnel on metallic 0}
                       ambient 0 diffuse 0.6 conserve_energy }  
      }
      interior{ ior 1.3 }
      // normal {bumps 0.1 scale 0.01}
     }
}
#end

// Include file for the macro
#include "skyrmion.inc"
