# convert-shpz.py


## How to run
This script will convert Z/M shapefiles (PointZ/M, PolyLineZ/M, PolygonZ/M, MultiPointZ/M) to normal shapefiles without Z/M-values.

The input shapefile(s) to be converted must be zipped.

Example below: convert the zip shapefiles in directory `d:\shapefiles` and output the result to `d:\output`
````
# convert-shpz.py requires the PyShp library (https://github.com/GeospatialPython/pyshp)
pip install requirements.txt

python convert-shpz.py -h
usage: convert-shpz.py [-h] [-i [INPUT]] [-o [OUTPUT]]

Convert Z/M shapefiles (PointZ/M, PolyLineZ/M, PolygonZ/M, MultiPointZ/M) to normal shapefiles without Z/M-values

optional arguments:
  -h, --help            show this help message and exit
  -i [INPUT], --input [INPUT]
                        Path to a zip shapefile or a directory containing them
  -o [OUTPUT], --output [OUTPUT]
                        Path to output directory for the converted shapefiles

Refer to https://github.com/geoenvo/convert-shpz for more details

python convert-shpz.py -i d:\shapefiles -o d:\output

# without -i and -o parameters the script will look for the input zip shapefiles in the current working directory
python convert-shpz.py
````
