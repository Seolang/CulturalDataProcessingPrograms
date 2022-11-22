import os
import re
import pandas as pd
import numpy as np

pd.set_option('display.max_row', 1000)
pd.set_option('display.max_columns', 1000)

# 초성 리스트. 00 ~ 18
CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
# 중성 리스트. 00 ~ 20
JUNGSUNG_LIST = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
# 종성 리스트. 00 ~ 27 + 1(1개 없음)
JONGSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

alphabet2 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

etc = ['`','~','!','@','#','$','%','^','&','*','-','=','+','[',']','{','}','\\','|','<','>',',','.','?','/']

check_error_word = [CHOSUNG_LIST, JUNGSUNG_LIST, JONGSUNG_LIST, alphabet, alphabet2, etc]


def data_check():
    excel_path = input("검수할 엑셀 파일 경로 : ")
    image_path = input("이미지 파일 경로(image 폴더가 있는 폴더의 경로) : ")


    if image_path[-1] != '\\':
        image_path = image_path + '\\'

    # official_path = 'C:\\Users\\USER v2.7\\Desktop\\원형기록 로컬\\20221011_국가민속문화재_사업정보.xlsx'
    # check_path = 'C:\\Users\\USER v2.7\\Desktop\\원형기록 로컬\\이미지메타데이터_우승빈.xlsx'
    # image_path = "C:\\Users\\USER v2.7\\Desktop\\원형기록 로컬\\서문성벽집\\이미지\\"
    # cul_code = 1483600990000

    excel = pd.read_excel(excel_path)



    cul_category = sido_excel['시도'].values[0] + "유형문화재"
    cul_name = sido_excel['문화재명'].values[0]
    cul_number = sido_excel['지정번호'].values[0]
    cul_record_name = sido_excel['기록화사업명'].values[0]
    cul_biz_code = sido_excel['사업유형코드'].values[0]
    cul_id = sido_excel['사업아이디'].values[0]
    cul_act_comp = sido_excel['수행업체명'].values[0]

    filePath = image_path + cul_category + '\\' + cul_category + '_' + cul_number + '_' + cul_name.replace(" ", "_") + '\\' + cul_record_name.replace(" ", "_") + '\\' + "이미지" + '\\'
    pathList = [filePath + "원본\\", filePath + "서비스\\", filePath + "썸네일\\"]
    o_path = pathList[0][pathList[0].find("이미지"):]
    s_path = pathList[1][pathList[1].find("이미지"):]
    t_path = pathList[2][pathList[2].find("이미지"):]
    original_photos = []
    service_photos = []
    thumbnail_photos = []

    prefix = cul_category + '_' + cul_number + '_' + cul_name.replace(" ", "_")

    try:
        files = os.listdir(image_path)
        print("이미지 폴더 경로 확인")
    except:
        print("이미지 폴더에 접근할 수 없습니다. 폴더 계층이 잘못되었습니다.")
        exit()

    try:
        original_photos = [pic for pic in os.listdir(pathList[0]) if pic != "Thumbs.db"]
        service_photos = [pic for pic in os.listdir(pathList[1]) if pic != "Thumbs.db"]
        thumbnail_photos = [pic for pic in os.listdir(pathList[2]) if pic != "Thumbs.db"]
        print("이미지 불러오기 완료")
    except:
        print("원본, 서비스 또는 썸네일 폴더가 존재하지 않거나 경로가 잘못 되었습니다.")
        exit()





    print("각 항목 파일 수량 및 이름일치 검증 : ", end='')
    if len(original_photos) == len(service_photos) and len(original_photos) == len(thumbnail_photos):
        err = [[x, y, z] for [idx, x], y, z in zip(enumerate(original_photos), service_photos, thumbnail_photos) if
               not x == y and x == z]
        if err:
            print("각 항목 파일의 이름 중 일치하지 않는것이 존재합니다.")
            for e in err:
                print("\t번호 " + str(e[0]) + '\t오류내용 : ' + str(e[1]) + ' -> ' + str(e[2]))
            print()

        else:
            print("이상 없음")
    else:
        print("각 항목의 사진 수량이 다릅니다")
        exit()



    print("\n===엑셀 파일 검사중===")
    err = [[idx+3, x, cul_category] for idx, x in enumerate(chk_excel['문화재유형'].values[1:]) if x != cul_category]
    if len(err) != 0:
        print("문화재 유형 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t\t오류내용 : ' + str(e[1]) + ' -> ' + str(e[2]))
        print()

    err = [[idx+3, x, cul_number] for idx, x in enumerate(chk_excel['지정번호'].values[1:]) if x != cul_number]
    if len(err) != 0:
        print("\n지정번호 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t\t오류내용 : ' + e[1] + ' -> ' + str(e[2]))
        print()

    err = [[idx+3, x, cul_code] for idx, x in enumerate(chk_excel['문화재번호'].values[1:]) if str(x) != str(cul_code)]
    if len(err) != 0:
        print("\n문화재 번호 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t오류내용 : ' + str(e[1]) + ' -> ' + str(e[2]))
        print()

    err = [[idx+3, x, cul_name] for idx, x in enumerate(chk_excel['문화재명'].values[1:]) if x != cul_name]
    if len(err) != 0:
        print("\n문화재 명 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t오류내용 : ' + e[1] + ' -> ' + str(e[2]))
        print()

    err = [[idx+3, x, cul_id] for idx, x in enumerate(chk_excel['기록화사업ID'].values[1:]) if x != cul_id]
    if len(err) != 0:
        print("\n기록화사업ID 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t오류내용 : ' + e[1] + ' -> ' + str(e[2]))
        print()

    err = [[idx+3, x, cul_record_name] for idx, x in enumerate(chk_excel['사업명'].values[1:]) if x != cul_record_name]
    if len(err) != 0:
        print("\n사업명 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t오류내용 : ' + e[1] + ' -> ' + str(e[2]))
        print()

    err = [[idx+3, x] for idx, x in enumerate(chk_excel['건조물번호'].values[1:]) if x != 1]
    if len(err) != 0:
        print("\n건조물 번호 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t오류내용 : ' + e[1]+ ' -> ' + '1')
        print()

    err = [[idx+3, x, cul_name] for idx, x in enumerate(chk_excel['건조물명'].values[1:]) if x != cul_name]
    if len(err) != 0:
        print("\n건조물명 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t오류내용 : ' + e[1] + ' -> ' + str(e[2]))
        print()

    err = [[idx+3, x, idx+1] for idx, x in enumerate(chk_excel['일련번호'].values[1:]) if x != (idx+1)]
    if len(err) != 0:
        print("\n일련번호 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t오류내용 : ' + str(e[1]) + ' -> ' + str(e[2]))
        print()

    years = cul_id[3:7]
    err = [[idx+3, x, years] for idx, x in enumerate(chk_excel['생산연도'].values[1:]) if str(x) != str(years)]
    if len(err) != 0:
        print("\n생산 연도 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t오류내용 : ' + str(e[1]) + ' -> ' + str(e[2]))
        print()

    if np.isnan(cul_act_comp):
        err = [[idx + 3, x, "알수없음"] for idx, x in enumerate(chk_excel['수행기관'].values[1:]) if x != "알수없음"]
    else:
        err = [[idx + 3, x, cul_act_comp] for idx, x in enumerate(chk_excel['수행기관'].values[1:]) if x != cul_act_comp]
    if len(err) != 0:
        print("\n수행기관 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t오류내용 : ' + str(e[1]) + ' -> ' + str(e[2]))
        print()


    err = []
    for [idx, x], y in zip(enumerate(chk_excel['원본파일명'].values[1:]), original_photos):
        temp = ""
        if prefix not in x or prefix not in y:
            temp += "파일명 형식 오류, "
        if x != y:
            temp += "엑셀 - 파일명 비일치, "
        if x.find(' ') != -1:
            temp += "공백 포함, "

        for arr in check_error_word:
            stop = False
            for s in arr:
                if s in x[:x.rfind('.')] or s in y[:y.rfind('.')-1]:
                    temp += "오탈자 기입"
                    stop = True
                    break
            if stop:
                break

        if temp:
            temp = '<' + temp + '>'
            err.append([idx, x, y, temp])

    if len(err) != 0:
        print("\n원본 파일명 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t오류내용 : (엑셀)' + str(e[1]) + ' | (파일)' + str(e[2]) + '\t' + str(e[3]))
        print()

    fileExt = [l[l.rfind('.') + 1:] for l in original_photos]

    err = [[idx+3, x, y] for [idx, x], y in zip(enumerate(chk_excel['원본파일형태(FLFM)'].values[1:]), fileExt) if x.upper() != y.upper()]
    if len(err) != 0:
        print("\n파일 확장자 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t오류내용 : ' + str(e[1]) + ' -> ' + str(e[2]))
        print()

    err = [[idx+3, x, o_path] for idx, x in enumerate(chk_excel['원본파일경로'].values[1:]) if x != o_path]
    if len(err) != 0:
        print("\n원본 파일 경로 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t오류내용 : ' + str(e[1]) + ' -> ' + str(e[2]))
        print()

    err = [[idx+3, x, y] for [idx, x], y, z in zip(enumerate(chk_excel['제목'].values[1:]), chk_excel['내용'].values[1:], original_photos)
           if x not in z.replace('_', ' ') or x != y or re.search('\d', x) is not None]
    if len(err) != 0:
        print("\n제목, 내용 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t오류내용 : ' + str(e[1]) + ' | ' + str(e[2]))
        print()

    fileSize = [os.path.getsize(pathList[0] + l) for l in original_photos]
    err = [[idx+3, x, y] for [idx, x], y in zip(enumerate(chk_excel['원본파일크기(byte)'].values[1:]), fileSize) if x != y]
    if len(err) != 0:
        print("\n원본 파일 크기 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t오류내용 : ' + str(e[1]) + ' -> ' + str(e[2]))
        print()

    err = []
    for [idx, x], y in zip(enumerate(chk_excel['서비스파일명'].values[1:]), service_photos):
        temp = ""
        if prefix not in x or prefix not in y:
            temp += "파일명 형식 오류, "
        if x != y:
            temp += "엑셀 - 파일명 비일치, "
        if x.find(' ') != -1:
            temp += "공백 포함, "

        for arr in check_error_word:
            stop = False
            for s in arr:
                if s in x[:x.rfind('.')] or s in y[:y.rfind('.')]:
                    temp += "오탈자 기입"
                    stop = True
                    break
            if stop:
                break

        if temp:
            temp = '<' + temp + '>'
            err.append([idx, x, y, temp])

    if len(err) != 0:
        print("\n서비스 파일명 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t오류내용 : (엑셀)' + str(e[1]) + ' | (파일)' + str(e[2]) + '\t' + str(e[3]))
        print()


    err = [[idx+3, x, s_path] for idx, x in enumerate(chk_excel['서비스파일경로'].values[1:]) if x != s_path]
    if len(err) != 0:
        print("\n서비스 파일 경로 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t오류내용 : ' + str(e[1]) + ' -> ' + str(e[2]))
        print()

    err = [[idx+3, x, t_path] for idx, x in enumerate(chk_excel['썸네일파일경로'].values[1:]) if x != t_path]
    if len(err) != 0:
        print("\n썸네일 파일 경로 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t오류내용 : ' + str(e[1]) + ' -> ' + str(e[2]))
        print()

    biz_code = {10:"실측조사",
                12:"정밀실측조사",
                13:"정밀안전진단",
                14:"정밀조사",
                16:"콘텐츠제작",
                18:"기타"}
    biz_code_str = biz_code[cul_biz_code]
    err = [[idx+3, x, y, cul_biz_code, biz_code_str] for [idx, x], y in zip(enumerate(chk_excel['분류코드'].values[1:]), chk_excel['분류'].values[1:]) if not x == cul_biz_code and y ==biz_code_str]
    if len(err) != 0:
        print("\n분류코드, 분류 오류")
        for e in err:
            print("\t번호 " + str(e[0]) + '\t오류내용 : ' + str(e[1]) + ' | ' + str(e[2]) + ' -> ' + str(e[3]) + ' | ' + str(e[4]))
        print()

    print("검사가 끝났습니다.")