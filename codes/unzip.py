import os, shutil
import zipfile
from pathlib import Path

def unzipData():

        i = 1
        dpath = str(os.getcwd()) + r'\data\commonData\downloadData'
        upath = str(os.getcwd()) + r'\data\commonData\unzipData'
        if os.path.exists(upath):
            shutil.rmtree(upath)
        Path(upath).mkdir(parents=True, exist_ok=True)
        for file in os.listdir(dpath):
            try:
                with zipfile.ZipFile(dpath + '\\'+file, 'r') as zip_ref:
                    zip_ref.extractall(upath)
                print('File '+str(i)+' unzipped.')
                i=i+1

            except zipfile.BadZipFile:
                print(f"{dpath} + '\\' + {file} is not a valid ZIP archive.")
                continue

unzipData()