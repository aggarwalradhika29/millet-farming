import os, shutil
import geopandas as gpd
import rasterio
import rasterstats
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

def backscatterCurve(dataType):
    import warnings
    warnings.filterwarnings('ignore')
    polar = []
    for line in open((os.getcwd()) + r'\data\commonData\\polarization.txt','r').readlines():
        polar.append(line.strip())
    print("Polarization specified: ", polar)

    gpath = str(os.getcwd()) + r'\data\shapeFiles\\GT\\groundTruth.shp'
    data = gpd.read_file(gpath)
    data = data.to_crs(epsg = 4326)
    print(data.head())
    print(data.columns)
    print(data['name'].unique())
    grouped= data.groupby('name')
    # print(grouped)

    for key, values in grouped:
        ind_crop= values
        # print(key)

    print(type(ind_crop))
    result_folder= str(os.getcwd()) + r'\data\shapeFiles\\attribute_split\\'

    if os.path.exists(result_folder):
        shutil.rmtree(result_folder)
    Path(result_folder).mkdir(parents=True, exist_ok=True)

    for key, values in grouped:
        output_name= "%s.shp" % key.replace(" ", "_")
        print("Processing: %s" % key)

        outpath= os.path.join(result_folder, output_name)
        values.to_file(outpath)

    print(result_folder)

    path = result_folder
    shpList= []
    for i in os.listdir(path):
        if i.endswith('.shp'):
            j = path + '\\' + i
            shpList.append(j)

    print(shpList)
    for p in polar:
        rasterIn = rasterio.open(str(os.getcwd()) + r'\data\commonData\layerStack\\layerStacked' + str(p) + '.tif')
        zonal_path = str(os.getcwd()) + r'\data\shapeFiles\\zonal_stats\\' + str(p) + '\\'
        if os.path.exists(zonal_path):
            shutil.rmtree(zonal_path)
        Path(zonal_path).mkdir(parents=True, exist_ok=True)

        for k in range(len(shpList)):
            gdf= gpd.read_file(shpList[k])
            df = pd.DataFrame()
            for j in range(1, (rasterIn.count + 1)):
                band = rasterIn.read(j)
                affine = rasterIn.transform

                mean_stat = rasterstats.zonal_stats(gdf, band, affine = affine, stats = ['mean'], geojson_out = True)
                mean_crop = []
                i = 0
                while i<len(mean_stat):
                    mean_crop.append(mean_stat[i]['properties']['mean'])
                    i = i+1
                column_name = 'B' + str(j)
                df[column_name] = mean_crop

            df.to_excel(zonal_path + str(shpList[k].split('\\')[-1][:-4]) + '.xlsx')

            excelPath = str(os.getcwd()) + r'\data\shapeFiles\\zonal_stats\\'  + str(p) + '\\'
        xlList= []
        for i in os.listdir(excelPath):
            if i.endswith('.xlsx'):
                j = excelPath + '\\' + i
                xlList.append(j)

        print(xlList)
        crops = []
        for k in range(len(shpList)):
            crops.append(str(shpList[k].split('\\')[-1][:-4]))
        print(crops)

        bands = []
        for i in range(1, rasterIn.count + 1):
            # b = 'B' + str(i)
            bands.append('B' + str(i))

        print(bands)


        zonal_stats = pd.DataFrame()
        zonal_stats['Class'] = bands
        filename = str(os.getcwd()) + r'\\dates.txt'
        if(dataType == 'SENTINEL-1A'):
            
            with open(filename) as file:
                dates = [line.rstrip() for line in file]
            for i in range(len(dates)):
                dates[i]= dates[i][:-1]
            print(str(dates))
            print()
        else:
            with open(filename) as file:
                dates = [line.rstrip() for line in file]
            print(str(dates))
            print()
            print()

        zonal_stats['Class'] = dates

        for i in range(len(xlList)):
            df = pd.read_excel(xlList[i])
            df.drop(columns=df.columns[0], axis=1, inplace=True)
            meanList = []
            for j in bands:
                avg = df[j].mean()
                meanList.append(avg)
            zonal_stats[crops[i]] = meanList
            
        print(zonal_stats)
        zonal_stats.to_excel(zonal_path + r'zonal_stats.xlsx')

        
        fig, ax = plt.subplots(figsize= [20, 10])
        cols = list(zonal_stats)[1:]
        print(cols)
        for i in list(cols):
            ax.plot(zonal_stats['Class'], zonal_stats[i], linewidth = 2, label = i)

        ax.set_ylabel('Backscatter Coefficient (dB)', fontsize= 8)
        ax.set_xlabel('Date', fontsize= 8)
        titleText = 'Backscatter Coefficient Curve For Different Crops Using Band'
        plt.title(titleText, weight = 'bold', fontsize = 12)
        figure_size = plt.gcf().get_size_inches()
        factor = 0.38
        plt.gcf().set_size_inches(factor * figure_size)
        plt.legend( fontsize = '7')
        plt.savefig(zonal_path + r'backscatterCurve'  + str(p) + '.png', bbox_inches = 'tight', dpi= 200)
        plt.close(fig)


# backscatterCurve()