import os
import natsort
import sys

def extract_files_info():
    filePath = input("원본 파일 경로 : ")


    # if path end not finished with \, add it
    if filePath[-1] != '\\':
        filePath = filePath + '\\'


    fileList = os.listdir(filePath)
    fileList = [pic for pic in fileList if pic != "Thumbs.db"]
    fileList = natsort.natsorted(fileList)

    # original files extensions
    fileExt = [l[l.rfind('.') + 1:] for l in fileList]

    # original files size(bytes)
    fileSize = [os.path.getsize(filePath + l) for l in fileList]

    python_file_path = os.path.dirname(sys.executable)
    print("make file to " + python_file_path)
    # create txt files
    _name = open(python_file_path + '\\' + "file_name.txt", "w")
    _size = open(python_file_path + '\\' + "file_size.txt", 'w')
    _ext = open(python_file_path + '\\' + "file_ext.txt", 'w')

    # put datas in files
    for file in fileList:
        _name.writelines(file.strip() + '\n')

    for ext in fileExt:
        _ext.writelines(ext.strip() + '\n')

    for size in fileSize:
        _size.writelines(str(size).strip() + '\n')

    _name.close()
    _size.close()
    _ext.close()