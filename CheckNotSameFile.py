import os
import sys
import re
import collections

def extract_files_info():
    firstPath = input("첫번째 폴더 경로 : ")
    secondPath = input("두번째 폴더 경로 : ")

    # if path end not finished with \, add it
    if firstPath[-1] != '\\':
        firstPath = firstPath + '\\'

    if secondPath[-1] != '\\':
        secondPath = secondPath + '\\'


    fileList = os.listdir(firstPath)
    fileList = [pic[:pic.rfind('.')] for pic in fileList if pic != "Thumbs.db" and pic != "기타"]

    servList = os.listdir(secondPath)
    servList = [pic[:pic.rfind('.')] for pic in servList if pic != "Thumbs.db" and pic != "기타"]

    secondNotInFirst = [f for f in servList if f not in fileList]
    firstNotInSecond = [f for f in fileList if f not in servList]


    duple = []
    duple2 = []
    for f in fileList:
        if fileList.count(f) != 1:
            duple.append(f)

    duple = set(duple)

    for f in servList:
        if servList.count(f) != 1:
            duple2.append(f)

    duple2= set(duple2)

    python_file_path = os.path.dirname(sys.executable)
    # create txt files
    _name = open(python_file_path + '\\' + "First_Not_In_Second.txt", "w")
    _name2 = open(python_file_path + '\\' + "Second_Not_In_First.txt", "w")


    # put datas in files
    print('=======First files not in Second folder=======')
    for file in firstNotInSecond:
        print(file)
        _name.writelines(file.strip() + '\n')

    print('=======Second files not in First folder=======')
    for file in secondNotInFirst:
        print(file)
        _name2.writelines(file.strip() + '\n')

    if duple:
        print('=======Duple Files in First Folder=======')
        _name3 = open(python_file_path + '\\' + "First_File_Duplication.txt", "w")
        for file in duple:
            print(file)
            _name.writelines(file.strip() + '\n')
        _name3.close()

    if duple2:
        print('=======Duple Files in Second Folder=======')
        _name4 = open(python_file_path + '\\' + "Second_File_Duplication.txt", "w")
        for file in duple2:
            print(file)
            _name.writelines(file.strip() + '\n')
        _name4.close()
    print()
    _name.close()
    _name2.close()




def extract_files_info2():
    firstPath = input("도면 폴더 경로 : ")
    secondPath = input("엑셀 폴더 경로 : ")

    # if path end not finished with \, add it
    if firstPath[-1] != '\\':
        firstPath = firstPath + '\\'

    if secondPath[-1] != '\\':
        secondPath = secondPath + '\\'


    fileList = os.listdir(firstPath)
    fileList = [pic for pic in fileList if pic != "Thumbs.db" and pic != "기타"]

    servList = os.listdir(secondPath)
    servList = [pic for pic in servList if pic != "Thumbs.db" and pic != "기타"]

    folderDic = {}
    excelList = []
    excelDic = {}

    folderNum = 0
    excelNum = 0

    for f in fileList:
        count = 0
        innerfolders = 0

        if os.path.isdir(firstPath+f):
            innerfolders = len(os.listdir(firstPath+f+'\\'))

        for m in re.finditer('_', f):
            count += 1
            if count == 3:
                folderDic.setdefault(f[0:m.end()-1],0)
                folderDic[f[0:m.end()-1]] += innerfolders
                folderNum += innerfolders
                break

    for f in servList:
        search = False
        word = f
        count = 0
        for m in re.finditer('_', f):
            count += 1
            if count == 3:
                excelList.append(f[0:m.end()-1])
                break

    excelNum = len(excelList)
    excelDic = collections.Counter(excelList)

    print(f'도면 폴더 수 : {folderNum}')
    print(f'엑셀 파일 수 : {excelNum}')

    print("사업이 2개 이상인 폴더")
    for key, val in folderDic.items():
        if val > 1:
            print(f'{key} : {val}')

    print('\n===================')


    for key, val in folderDic.items():
        if not (key in excelDic.keys() and val == excelDic[key]):
            print(f'{key} : {val}')


    python_file_path = os.path.dirname(sys.executable)
    # create txt files
    #_name = open(python_file_path + '\\' + "First_Not_In_Second.txt", "w")


    print()
    #_name.close()
