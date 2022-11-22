import os
import re
import pandas as pd

def data_processing():
    filePath = input("이미지 파일 경로 : ")
    rmPrefix = input("교체할 Prefix 입력 : ")
    newPrefix = input("새로운 Prefix 입력 : ")
    errorList = []

    # if path end not finished with \, add it
    if filePath[-1] != '\\':
        filePath = filePath + '\\'

    pathList = [filePath + "원본\\", filePath + "서비스\\", filePath + "썸네일\\"]


    # change Image file names
    for path in pathList:  # per locations,
        fileList = os.listdir(path)
        fileList = [pic for pic in fileList if pic != "Thumbs.db"]

        # change each folder's file names
        for idx, f in enumerate(fileList):
            if rmPrefix not in f:
                errorList.append([f, idx + 1])
            os.rename(path + f, path + f.replace(rmPrefix, newPrefix).replace(" ", "_"))

    # original photo files
    fileList = os.listdir(pathList[0])
    fileList = [pic for pic in fileList if pic != "Thumbs.db"]

    # original files extensions
    fileExt = [l[l.rfind('.') + 1:] for l in fileList]

    # service photo files
    fileListService = os.listdir(pathList[1])
    fileListService = [pic for pic in fileListService if pic != "Thumbs.db"]

    # original files size(bytes)
    fileSize = [os.path.getsize(pathList[0] + l) for l in fileList]

    # original files details
    fileName = [l[:l.rfind('.')].replace(newPrefix, '').replace('_', ' ') for l in fileList]
    fileName = [re.sub('[0-9]+', '', n) for n in fileName]

    # create txt files
    _name = open(filePath + "file_name.txt", "w")
    _original = open(filePath + "file_original.txt", 'w')
    _services = open(filePath + "file_service.txt", 'w')
    _size = open(filePath + "file_size.txt", 'w')
    _ext = open(filePath + "file_ext.txt", 'w')
    if errorList:
        _error = open(filePath + "Error!!!!.txt", 'w')
        _error.writelines("몬가... 몬가 문제있음!\n\n===문제가 있는 항목들===\n\n")
        for err in errorList:
            _error.writelines('번호 : ' + str(err[1]) + '\t' + err[0].strip() + '\n')

        _error.close()

    # put datas in files
    for file in fileList:
        _original.writelines(file.strip() + '\n')

    for ext in fileExt:
        _ext.writelines(ext.strip() + '\n')

    for service in fileListService:
        _services.writelines(service.strip() + '\n')

    for name in fileName:
        _name.writelines(name.strip() + '\n')

    for size in fileSize:
        _size.writelines(str(size).strip() + '\n')

    _name.close()
    _original.close()
    _services.close()
    _size.close()
    _ext.close()