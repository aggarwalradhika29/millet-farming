# code to layer stack and mask the data bands
# import required libraries : Python 3.11.0
import os, shutil
import fiona
import rasterio
import rasterio.mask
from osgeo import gdal
from rasterio.crs import CRS
from pathlib import Path
from timeit import default_timer as timer

# function to layer stack all the subset tiles into a single multi-layered tif file
def layerStack():
    polar = ['VH']
    # for line in open((os.getcwd()) + r'\data\commonData\\polarization.txt','r').readlines():
    #     polar.append(line.strip())
    print("Polarization specified: ", polar)
    layeredPath = str(os.getcwd()) + r'\data\commonData\layerStack\\'
    if os.path.exists(layeredPath):
        shutil.rmtree(layeredPath)
    Path(layeredPath).mkdir(parents=True, exist_ok=True)

    start= timer()
    print(start)
    for p in polar:
        subPath = str(os.getcwd()) + r'\data\commonData\subset\\' + str(p)
        print(subPath)

        layersList= []
        for i in os.listdir(subPath):
            filename= subPath + '\\' + i
            layersList.append(filename)
        print(layersList)

        with rasterio.open(layersList[0]) as src0:
            meta= src0.meta
        meta.update(count= len(layersList))


        with rasterio.open(layeredPath + r'layerStacked' + str(p) + '.tif', 'w', **meta) as dest:
            for id, layer in enumerate(layersList, start= 1):
                with rasterio.open(layer) as src:
                    dest.write_band(id, src.read(1))

        with rasterio.open(layeredPath + r'layerStacked' + str(p) + '.tif') as stack:
            stackData= stack.read(masked= True)
            stackMeta= stack.profile

        print(stackMeta)

    endLayer= timer()
    print(endLayer)
    print('Total time elapsed for layer-stacking: ',endLayer-start)


# function to extract by mask the agricultural land specified by lulc shape file entered by the user
def cropMask():
    start= timer()
    print(start)
    polar = []
    for line in open((os.getcwd()) + r'\data\commonData\\polarization.txt','r').readlines():
        polar.append(line.strip())
    print("Polarization specified: ", polar)

    outPath= str(os.getcwd()) + r'\data\commonData\toClassify\\'
    if os.path.exists(outPath):
        shutil.rmtree(outPath)
    Path(outPath).mkdir(parents=True, exist_ok=True)

   

    shpin= str(os.getcwd()) + r'\data\shapeFiles\cropMask\\cropMask_projected.shp'
    print(shpin)

    with fiona.open(shpin, 'r') as shapefile:
        shapes= [feature['geometry'] for feature in shapefile]

    for p in polar:
        tifin = str(os.getcwd()) + r'\data\commonData\layerStack\\layerStacked' + str(p) + '.tif'

        with rasterio.open(tifin) as src:
            out_image, out_transform= rasterio.mask.mask(src, shapes, crop= True)
            out_meta= src.meta
        utm_crs = CRS.from_epsg(4326)

        out_meta.update(
            {
                "driver" : "GTiff",
                'crs': utm_crs,
                "nodata" : 0,
                "height" : out_image.shape[1],
                "width" : out_image.shape[2],
                "transform" : out_transform,
                
            }
        )

        target= outPath + 'cropMasked' + str(p) + '.tif'
        with rasterio.open(target, 'w', **out_meta) as dest:
            dest.write(out_image)

    end= timer()
    print(end)
    print('Total time elapsed for crop masking: ',end-start)

# crop mask for EOS-4
def cropMaskEOS4():
    start= timer()
    print(start)
    polar = []
    for line in open((os.getcwd()) + r'\data\commonData\\polarization.txt','r').readlines():
        polar.append(line.strip())
    print("Polarization specified: ", polar)

    outPath= str(os.getcwd()) + r'\data\commonData\toClassify\\'
    if os.path.exists(outPath):
        shutil.rmtree(outPath)
    Path(outPath).mkdir(parents=True, exist_ok=True)

   

    shpin= str(os.getcwd()) + r'\data\shapeFiles\cropMask\\cropMask_projected.shp'
    print(shpin)

    for p in polar:
        tifin = str(os.getcwd()) + r'\data\commonData\layerStack\\layerStacked' + str(p) + '.tif'
        target= outPath + 'cropMasked' + str(p) + '.tif'
        gdal.Warp(target, tifin, cutlineDSName = shpin, format="GTiff", cropToCutline = True)

    end= timer()
    print(end)
    print('Total time elapsed for crop masking: ',end-start)

layerStack()
# print(str(os.getcwd()))
# cropMask()