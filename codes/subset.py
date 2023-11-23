# code to subset the mosaic-ed tiles according to the region of interest, extract by mask
# import required libraries : Python 3.11.0
from osgeo import gdal
from timeit import default_timer as timer
start= timer()
print(start)
import os, shutil
from pathlib import Path

# function to extract area by mask
def district_mask():
    polar = ['VH']
    # for line in open((os.getcwd()) + r'\data\commonData\\polarization.txt','r').readlines():
    #     polar.append(line.strip())
    print("Polarization specified: ", polar)

    for p in polar:
        prevPath= str(os.getcwd()) + r'\data\commonData\mosaic\\' + str(p) + '\\'
        outPath= str(os.getcwd()) + r'\data\commonData\subset\\' + str(p) + '\\'
        if os.path.exists(outPath):
            shutil.rmtree(outPath)
        Path(outPath).mkdir(parents=True, exist_ok=True)

        shpPath = str(os.getcwd()) + r'\data\shapeFiles\AOI'
        shpin = ''
        for i in os.listdir(shpPath):
            if i.endswith('.shp'):
                shpin = shpPath + '\\' + i

        print(shpin)                                    # shape file of area of interest

        ctr= 0
        for path in os.listdir(prevPath):
            if os.path.isfile(os.path.join(prevPath, path)):
                ctr += 1
        print('Files in mosaic folder: ', ctr)

        lines_1 = []
        for i in os.listdir(prevPath):
            rasin= str(prevPath) +'\\'+ str(i)
            print(str(rasin[-13:-4]))
            output= outPath + 'subset' + rasin[-13:]
            lines_1.append(str(rasin[-13:-4]))
            # print(output)

            gdal.Warp(output, rasin, cutlineDSName = shpin, format="GTiff", cropToCutline = True)
            # using gdal, on every mosaic-ed tile, subset is being performed

        with open ('dates.txt', 'w') as file:  
            for line_1 in lines_1:  
                file.write(line_1)  
                file.write('\n')  

    end= timer()
    print(end)
    print('Total time elapsed for subsetting: ',end-start)

district_mask()