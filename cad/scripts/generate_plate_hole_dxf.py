"""
Generates a SVG file for the plate holes
Pass the *.kicad_pcb file to this script to read the footprint locations of all MountingHoles

Should only be used for visual verification, since we want to produce the plate as a PCB,
we'll opt to create a netlist to import into KiCAD instead of using this.
"""

from argparse import ArgumentParser
from extract_footprint_positions import extract_footprint_positions
import subprocess

DRILL_SIZE = 4.5 # TODO: Adjust to the actual required value

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("pcb_file")
    parser.add_argument("svg_file")
    
    args = parser.parse_args()

    _, mount_locations, _, _ = extract_footprint_positions(open(args.pcb_file))

    out = open(args.svg_file, "w")
    out.write('<svg xmlns="http://www.w3.org/2000/svg">')
    for (x, y) in mount_locations:
        out.write(f'<circle cx="{x}mm" cy="{y}mm" r="{DRILL_SIZE/2}mm" fill="none" stroke-width="0.2mm" stroke="black"/>')
    out.write('</svg>')
