import os

def ordering():
    path = input('파일 위치 : ')
    rmPrefix = input('Prefix : ')

    if path[-1] != '\\':
        path = path + '\\'

    fileList = os.listdir(path)
    fileList = [pic for pic in fileList if pic != "Thumbs.db"]
    zerofill = len(str(len(fileList)))


    # change each folder's file names
    for idx, f in enumerate(fileList):
        os.rename(path + f,
                  path + f.replace(rmPrefix, rmPrefix + str(idx + 1).zfill(zerofill) + '_').replace(" ", "_"))