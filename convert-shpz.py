#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import logging
import shutil
import zipfile
import argparse

import shapefile


# pyshp constants for shapefiles with z/m information
SHP_POINT = 1
SHP_POLYLINE = 3
SHP_POLYGON = 5
SHP_MULTIPOINT = 8
SHP_POINTZ = 11
SHP_POLYLINEZ = 13
SHP_POLYGONZ = 15
SHP_MULTIPOINTZ = 18
SHP_POINTM = 21
SHP_POLYLINEM = 23
SHP_POLYGONM = 25
SHP_MULTIPOINTM = 28
SHP_MAP_Z_TO_NORMAL = {
    SHP_POINTZ: SHP_POINT,
    SHP_POLYLINEZ: SHP_POLYLINE,
    SHP_POLYGONZ: SHP_POLYGON,
    SHP_MULTIPOINTZ: SHP_MULTIPOINT,
    SHP_POINTM: SHP_POINT,
    SHP_POLYLINEM: SHP_POLYLINE,
    SHP_POLYGONM: SHP_POLYGON,
    SHP_MULTIPOINTM: SHP_MULTIPOINT
}


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(
            description='Convert Z/M shapefiles (PointZ/M, PolyLineZ/M, PolygonZ/M, MultiPointZ/M) to normal shapefiles without Z/M-values',
            epilog='Refer to https://github.com/geoenvo/convert-shpz for more details')
        parser.add_argument('-i', '--input', help='Path to a zip shapefile or a directory containing them', type=str, nargs='?', default='.')
        parser.add_argument('-o', '--output', help='Path to output directory for the converted shapefiles', type=str, nargs='?', default='output')
        args = parser.parse_args()
        input_zip_shp_path = args.input
        temp_dir = args.output
        zip_shp_file_paths = []
        #temp_dir = 'output'
        #temp_dir = 'd:\\output'
        #input_zip_shp_path = 'd:\\pyshp\\z shps\\'
        #input_zip_shp_path = 'd:\\pyshp\\z shps\\Rawan_Bencana_Gempa_Bumi_AR.zip'
        output_dir = 'converted' # directory to save the conversion result zip file
        # process single zip shp file or a directory containing multiple zip shp files
        if os.path.isfile(input_zip_shp_path) and input_zip_shp_path.lower().endswith('zip'):
            zip_shp_file_paths.append(input_zip_shp_path)
        elif os.path.isdir(input_zip_shp_path):
            # look for zip shp files in the directory
            zip_shp_file_paths = glob.glob(os.path.join(input_zip_shp_path, '*.zip'))
        if not zip_shp_file_paths:
            print('ERROR: invalid input file/directory, did not find any zip files to process')
            sys.exit()
        else:
            print('PROCESSING:\n- {}'.format('\n- '.join(zip_shp_file_paths)))
        count_shapefile_convert_success = 0
        count_shapefile_convert_skipped = 0
        count_shapefile_convert_error = 0
        count_shapefile_total = 0
        for zip_shp_file_path in zip_shp_file_paths:
            input_zip_filename = os.path.basename(zip_shp_file_path)
            temp_extract_dir = os.path.join(temp_dir, input_zip_filename)
            temp_output_dir = os.path.join(temp_extract_dir, output_dir)
            print('START: extracting "{}" to temporary directory'.format(input_zip_filename))
            with zipfile.ZipFile(zip_shp_file_path, 'r') as zip_input:
                # Extract all the contents of zip file to temporary directory
                zip_input.extractall(temp_extract_dir)
                shp_extracted_path = glob.glob(os.path.join(temp_extract_dir, '*.shp'))
                # process if there is only 1 shp file extracted from the zip
                if shp_extracted_path and len(shp_extracted_path) == 1:
                    shp_read = shapefile.Reader(shp_extracted_path[0])
                    output_shp_filename = os.path.basename(shp_extracted_path[0])
                    if shp_read.shapeType in SHP_MAP_Z_TO_NORMAL.keys():
                        print('CONVERTING: "{}" shapefile from Z/M type to normal shapefile'.format(output_shp_filename))
                        shp_write = shapefile.Writer(os.path.join(temp_output_dir, output_shp_filename))
                        if shp_read.shapeType == SHP_POINTZ:
                            shp_write.shapeType = SHP_MAP_Z_TO_NORMAL[SHP_POINTZ]
                        elif shp_read.shapeType == SHP_POLYLINEZ:
                            shp_write.shapeType = SHP_MAP_Z_TO_NORMAL[SHP_POLYLINEZ]
                        elif shp_read.shapeType == SHP_POLYGONZ:
                            shp_write.shapeType = SHP_MAP_Z_TO_NORMAL[SHP_POLYGONZ]
                        elif shp_read.shapeType == SHP_MULTIPOINTZ:
                            shp_write.shapeType = SHP_MAP_Z_TO_NORMAL[SHP_MULTIPOINTZ]
                        elif shp_read.shapeType == SHP_POINTM:
                            shp_write.shapeType = SHP_MAP_Z_TO_NORMAL[SHP_POINTM]
                        elif shp_read.shapeType == SHP_POLYLINEM:
                            shp_write.shapeType = SHP_MAP_Z_TO_NORMAL[SHP_POLYLINEM]
                        elif shp_read.shapeType == SHP_POLYGONM:
                            shp_write.shapeType = SHP_MAP_Z_TO_NORMAL[SHP_POLYGONM]
                        elif shp_read.shapeType == SHP_MULTIPOINTM:
                            shp_write.shapeType = SHP_MAP_Z_TO_NORMAL[SHP_MULTIPOINTM]
                        # copy shapefile
                        shp_write.fields = shp_read.fields[1:]
                        for shp_record in shp_read.iterShapeRecords():
                            # also update the shapeType of each shape record
                            shp_record.shape.shapeType = shp_write.shapeType
                            shp_write.record(*shp_record.record)
                            shp_write.shape(shp_record.shape)
                        shp_write.close()
                        shp_read.close()
                        # copy all extracted files except shp, shx, and dbf to output directory
                        extracted_all = glob.glob(os.path.join(temp_extract_dir, '*.*'))
                        extracted_shp = glob.glob(os.path.join(temp_extract_dir, '*.shp'))
                        extracted_dbf = glob.glob(os.path.join(temp_extract_dir, '*.dbf'))
                        extracted_shx = glob.glob(os.path.join(temp_extract_dir, '*.shx'))
                        files_to_copy = list(set(extracted_all) - set(extracted_shp) - set(extracted_dbf) - set(extracted_shx))
                        for file_to_copy in files_to_copy:
                            shutil.copy2(file_to_copy, temp_output_dir)
                        # finally zip the output files
                        files_to_zip = glob.glob(os.path.join(temp_output_dir, '*.*'))
                        output_zip_shp_path = os.path.join(temp_output_dir, input_zip_filename)
                        if os.path.isfile(output_zip_shp_path):
                            count_shapefile_convert_error += 1
                            print('ERROR: output zip file "{}" already exists'.format(output_zip_shp_path))
                        else:
                            # max zip compression level
                            with zipfile.ZipFile(output_zip_shp_path, 'w', zipfile.ZIP_DEFLATED, 9) as zip_output:
                                # Add files to the zip
                                for file_to_zip in files_to_zip:
                                    zip_output.write(file_to_zip, os.path.basename(file_to_zip))
                            count_shapefile_convert_success += 1
                            print('SUCCESS: converted "{}" shapefile from Z/M type to normal shapefile'.format(output_shp_filename))
                    else:
                        count_shapefile_convert_skipped += 1
                        print('SKIPPING: "{}" shapefile is not a Z/M type'.format(output_shp_filename))
                else:
                    count_shapefile_convert_error += 1
                    print('ERROR: found more than 1 extracted .shp file in "{}"'.format(temp_extract_dir))
            count_shapefile_total += 1
        print('SUMMARY')
        print('Shapefile converted\t: {}'.format(count_shapefile_convert_success))
        print('Shapefile skipped\t: {}'.format(count_shapefile_convert_skipped))
        print('Shapefile convert error\t: {}'.format(count_shapefile_convert_error))
        print('Shapefile total\t\t: {}'.format(count_shapefile_total))
        sys.exit(0)
    except Exception as e:
        print('ERROR: {}'.format(e))
        sys.exit()
