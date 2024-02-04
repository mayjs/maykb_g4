// The case side to build
case_side = "left"; // [left, right]

// The part of the case to build
case_part = "case"; // [case, bar]

// The general amount of wiggle-room
play = .2;

// The amount of wiggle-room around the pcb and plate in the case
case_play = .8;

// The thickness of the outer case wall
wall_thickness = 2.5; // 0.1

// The drill diameter for the screw inserts
screw_insert_dia = 3.2;

// The length of the hole for the screw inserts
screw_insert_hole_length = 6.5;

// The total height of the plate-pcb sandwich
plate_pcb_height = 6.6;

// The diameter of the audio plug
audio_plug_dia = 6.2;

// The diameter of the mount holes for the angle bar
screw_insert_angle_bar_dia = 4.1;

// The length of the hole to mount the angle bar
screw_insert_angle_bar_hole_length = 5;

// The width of the angle bar
angle_bar_width = 10;

// The maximum allowed width for the bar (this should be larger than the keyboard / case)
max_bar_length = 300;

// the height of the angle bar (this must be at least angle_bar_width / 2)
angle_bar_height = 14;

// The diameter of the rubber bumpers
bumper_dia = 8;

$fn = 100;

is_left = case_side == "left" ? true : false;

edge_file = is_left ? "left/left_pcb-Edge_Cuts.dxf" : "right/right_pcb-Edge_Cuts.dxf";

use <left/coordinates.scad>
use <right/coordinates.scad>

mount_positions = is_left ? kb_mount_centers_left() : kb_mount_centers_right();
jack_positions = is_left ? [max(audio_jack_x_left())] : [min(audio_jack_x_right())];
usb_c_position = is_left ? usb_c_x_left() : usb_c_x_right();
angle_bar_mount_positions = is_left ? [50, 135] : [75, 170, 210];
bumper_mount_positions = is_left ? [34, 80, 120, 160] : [48, 100, 150, 230];

angle_bar_y_position = -min([for(pos = mount_positions) pos.y]);

usb_c_jack_bounds = [10, 4];
 
use <mayscadlib/2d/shapes.scad>
use <mayscadlib/3d/screws.scad>
use <mayscadlib/positioning.scad>

module outline() {
    offset(delta=case_play)
    import(edge_file);
}

module wall_2d() {
  difference() {
    offset(r=wall_thickness)
    outline();
    outline();
  }
}

module bare_case() {
    linear_extrude(wall_thickness) {
        wall_2d();
        outline();
    }

    linear_extrude(wall_thickness + screw_insert_hole_length + plate_pcb_height)
    wall_2d();
}

module mounting_post() {
    linear_extrude(screw_insert_hole_length)
    difference() {
        circle(r=screw_insert_dia/2 + wall_thickness);
        circle(r=screw_insert_dia/2);
    }
}

module mounts() {
    for(pos = mount_positions) {
        translate([pos.x, -pos.y, wall_thickness - .0001]) {
            mounting_post();        
        }
    }
}

module connector_cutouts() {
    // usb-c
    bounds_with_play = usb_c_jack_bounds + [2*play, 2*play];
    translate([usb_c_position.x, 0, wall_thickness + screw_insert_hole_length - bounds_with_play.y/2])
    rotate([90,0,0])
    linear_extrude(100)
    rounded_square(bounds_with_play, corner_rad=1, center=true);

    // audio jack
    for(pos = jack_positions) {
        rad = audio_plug_dia/2 + play/2;
        translate([pos, 0, wall_thickness + screw_insert_hole_length - rad])
        rotate([90,0,0])
        cylinder(r=rad, 100);
    }
}

module case_with_angle_bar_mounts() {
    difference() {
        union() {
            bare_case();
            for(mx = angle_bar_mount_positions) {
                translate([mx, angle_bar_y_position, wall_thickness - .0001])
                cylinder(r=screw_insert_angle_bar_dia/2 + wall_thickness, h=screw_insert_angle_bar_hole_length);
            }
        }
        for(mx = angle_bar_mount_positions) {
            translate([mx, angle_bar_y_position, -.0001])
            cylinder(r=screw_insert_angle_bar_dia/2, h=screw_insert_angle_bar_hole_length);
        }
    }
}

module full_case() {
    difference() {
        case_with_angle_bar_mounts();
        connector_cutouts();
    }
    mounts();
}

module bar() {
    screw = m3_din912_cylinder_head(angle_bar_height * 2);

    bumper_plateau_inv_height = sqrt(pow(angle_bar_width/2, 2) - pow(bumper_dia/2, 2));
    bumper_plateau_height = angle_bar_width/2 - bumper_plateau_inv_height;

    difference() {
        intersection() {
            translate([0, angle_bar_y_position, angle_bar_width/2])
            rotate([90,0,90])
            linear_extrude(max_bar_length) {
                difference() {
                    circle(r=angle_bar_width/2); 
                    translate([-angle_bar_width,0])
                    square([angle_bar_width *2, angle_bar_width]);
                }

                translate([-angle_bar_width / 2, 0])
                square([angle_bar_width, angle_bar_height - angle_bar_width / 2]);
            }

            linear_extrude(max_bar_length + 1) {
                outline();
                wall_2d();
            }
        }

        for(mx = angle_bar_mount_positions) {
            translate([mx, angle_bar_y_position, angle_bar_height - screw_head_h(screw) - wall_thickness])
            mirror([0,0,1]) 
            make_screw(screw, head_clearance=angle_bar_width);

        }

        translate([0, angle_bar_y_position, -.0001])
        place([for (bx=bumper_mount_positions) [bx, 0]])
        cylinder(r=bumper_dia/2, h=bumper_plateau_height);
    }
}

if(case_part == "case") {
    full_case();
} else if (case_part == "bar") {
    bar(); 
}

