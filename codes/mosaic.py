# code to mosaic the preprocessed data tiles according to corresponding dates of pass
# import required libraries : Python 3.11.0
import os, gc, shutil, rasterio
from pathlib import Path
from rasterio.merge import merge
from timeit import default_timer as timer
from rasterio.crs import CRS

# function to mosaic the tiles with same date of pass
def mosaicTiles():
    start= timer()
    print(start)

    polar = ['VH']
    # for line in open((os.getcwd()) + r'\data\commonData\\polarization.txt','r').readlines():
    #     polar.append(line.strip())
    print("Polarization specified: ", polar)

    for p in polar:
        prevPath = str(os.getcwd()) + r'\data\commonData\toPreprocess\\' + str(p) + '\\'
        outPath = str(os.getcwd()) + r'\data\commonData\mosaic\\' + str(p) + '\\'
        if os.path.exists(outPath):
            shutil.rmtree(outPath)
        Path(outPath).mkdir(parents=True, exist_ok=True)
        ctr = 0
        for path in os.listdir(prevPath):
            if os.path.isfile(os.path.join(prevPath, path)):
                ctr += 1
        print('Files in the folder to be mosaiced: ', ctr)

        for file in os.listdir(prevPath):
            products = []
            for file1 in os.listdir(prevPath): 
                if str(file[:9]) == str(file1[:9]):
                    print(file1)
                    gc.enable()
                    products.append((prevPath + '\\' + file))
                    products.append((prevPath + '\\' + file1))

                    mosaic, output = merge(products)                                            # merge the products
                    raster = rasterio.open(products[0])                         
                    output_meta = raster.meta.copy()
                    utm_crs = CRS.from_epsg(4326)
                    output_meta.update(
                        {"driver": "GTiff",
                            "height": mosaic.shape[1],
                            "width": mosaic.shape[2],
                            "transform": output
                        }
                    )
                    with rasterio.open(outPath + '\mosaic' + str(file[:9]) + '.tif', 'w', **output_meta) as m:
                        m.write(mosaic)


                
    end= timer()
    print('time elapsed for mosaicing: ', (end-start))


mosaicTiles()