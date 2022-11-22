import os

def prefixChanger():

    do = {'서울' : '서울특별시',
          '경기' : '경기도',
          '강원' : '강원도',
          '경남' : '경상남도',
          '경북' : '경상북도',
          '전남' : '전라남도',
          '전북' : '전라북도',
          '충남' : '충청남도',
          '충북' : '충청북도',
          '인천' : '인천광역시',
          '광주' : '광주광역시',
          '대전' : '대전광역시',
          '울산' : '울산광역시'
          }


    filePath = input("파일 경로 : ")

    # if path end not finished with \, add it
    if filePath[-1] != '\\':
        filePath = filePath + '\\'

    # change Image file names
    fileList = os.listdir(filePath)
    fileList = [pic for pic in fileList if pic != "Thumbs.db"]
    check_1 = True
    check_mohyung = True

    # change each folder's file names
    for f in fileList:
        filename = f
        pref = f[:f.find('_')]
        city = pref[:2]
        if city in do.keys() and pref != do[city]:
            number = pref[4:]
            stringBuilder = do[city] + '_' + '유형문화재_' + '제' + str(number) + '호'
            filename = f.replace(pref, stringBuilder)

        os.rename(filePath + f, filePath + filename.replace(" ", "_"))
        if '_1.jpg' not in f:
            check_1 = False

    if check_1:
        fileList = os.listdir(filePath)
        fileList = [pic for pic in fileList if pic != "Thumbs.db"]

        for f in fileList:
            os.rename(filePath + f, filePath + f.replace("_1.jpg", ".jpg"))

    fileList = os.listdir(filePath)
    fileList = [pic for pic in fileList if pic != "Thumbs.db"]

    for f in fileList:
        os.rename(filePath + f, filePath + f.replace("-모형.jpg", ".jpg"))
