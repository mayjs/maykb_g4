#!/bin/sh

set -e

cd "${0%/*}"

SCAD_FILE="./case.scad"
PARAM_FILE="./case.json"

openscad -p "$PARAM_FILE" -P "Left Case" -o ./left/left_case.amf "$SCAD_FILE"
openscad -p "$PARAM_FILE" -P "Right Case" -o ./right/right_case.amf "$SCAD_FILE"
openscad -p "$PARAM_FILE" -P "Left Bar" -o ./left/left_bar.amf "$SCAD_FILE"
openscad -p "$PARAM_FILE" -P "Right Bar" -o ./right/right_bar.amf "$SCAD_FILE"
