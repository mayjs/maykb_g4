use <mayscadlib/2d/shapes.scad>
use <mayscadlib/positioning.scad>

$fn = 100;

hole_dims = [26.67, 9.652];
lip = 2;
thickness = 1.6;

linear_extrude(thickness)
rounded_square(hole_dims + [lip*2, lip*2], corner_rad=2, center=true);

lift(thickness)
linear_extrude(thickness)
rounded_square(hole_dims, center=true);
