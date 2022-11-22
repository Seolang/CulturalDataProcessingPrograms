import os
import pandas as pd
import numpy as np

pd.set_option('display.max_row', 1000)
pd.set_option('display.max_columns', 1000)


def check_excel_between():
    check_excel = "C:\\Users\\USER v2.7\\Desktop\\check_excel.xlsx"
    target_excel = "C:\\Users\\USER v2.7\\Desktop\\target_excel.xlsx"


    print("엑셀 파일을 불러오는중....")
    check = pd.read_excel(check_excel).astype('string')
    target = pd.read_excel(target_excel).astype('string')
    check = check.drop_duplicates()

    text = open("C:\\Users\\USER v2.7\\Desktop\\excelResult.txt", 'w')
    count = 1
    for l in target.values:
        check_l = check[(check['지정번호'] == l[0]) & (check['문화재번호'] == l[1]) & (check['기록화사업ID'] == l[3])]
        if not check_l.empty:
            if l in check_l.values:
                text.writelines("1\n")
                print(count, 'O')
            else:
                text.writelines("###UNEQUAL NAME###\n")
                print(count, 'Name')
        else:
            text.writelines("\n")
            print(count, 'X')

        count += 1


    text.close()
