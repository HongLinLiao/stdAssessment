# pip install pdfplumber
import pdfplumber

from dataModel import BasicModel as basicModel
from dataModel import ScoreModel as scoreModel
from sysException import sysException


def parse(path):

    # Basic Model
    id = path.split('/')[len(path.split('/'))-1].split('.')[0]
    name = ''
    isOk = True
    message = ''

    # Score Model
    score = ['']*15

    try:
        pdf = pdfplumber.open(path)

        for page in pdf.pages:

            # 獲取當前頁面的全部文字資訊，包括表格中的文字
            allText = page.extract_text()

            if(isinstance(allText, str)):
                # 找到成績單頁面
                if(allText.find('成 績 證 明 書') != -1 or allText.find('成績證明書') != -1):

                    if(allText.find('臺北市立') != -1):
                        # 臺北市立高中 Layout

                        # 基本資料
                        basicTable = page.extract_tables()[0][0]
                        # stName
                        name = basicTable[3]

                        # 成績
                        scoreTable = page.extract_tables()[1]

                        # 全校
                        schoolScore = scoreTable[len(scoreTable)-1]

                        # 個人
                        personScore = scoreTable[len(scoreTable)-2]

                        for i in range(5):
                            score[0 + 3*i] = round(float(personScore[5 + (i*7)]), 2)
                            score[1 + 3*i] = round(float(personScore[6 + (i*7)]), 2)
                            score[2 + 3*i] = round(float(personScore[7 + (i*7)]), 2)

                    else:
                        isOk=False
                        message='該學生所屬高中並未設定Layout!'

                    break
        # 找不到需要資料的情況
        if(isOk == True and name == ''):
            isOk=False
            message='找不到該學生之成績單頁面!'

    except Exception as e:
        name=''
        isOk=False
        message=sysException(e)
    finally:
        pdf.close()

    return basicModel(id, name, isOk = isOk, message = message), scoreModel(score)
