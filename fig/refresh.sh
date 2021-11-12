#!/usr/bin/env bash
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

PLOT_DIR="$SCRIPT_DIR/../sketch/plot"

rm grid/*
cp -t grid/ $PLOT_DIR/grid/hexagon/*.png
cp -t grid/ $PLOT_DIR/grid/triangle/*.png

rm bandgap/*
cp -t bandgap/ $PLOT_DIR/bandgap/*.png

rm matrix_eigen_value/*
cp $PLOT_DIR/matrix_sym/hexagon/summary.png matrix_eigen_value/summary_hexagon.png
cp $PLOT_DIR/matrix_sym/triangle/summary.png matrix_eigen_value/summary_triangle.png

rm wavepackages.png
cp -t . $PLOT_DIR/wavepackage/wavepackages.png