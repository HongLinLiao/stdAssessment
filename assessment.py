# pip install pdfplumber
import pdfplumber
import math

from dataModel import BasicModel as basicModel
from dataModel import ScoreModel as scoreModel
from sysException import sysException


def parse(path):

    # Basic Model
    id = path.split('/')[len(path.split('/'))-1].split('.')[0]
    school = ''
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

                    # 臺北市立高中
                    if(allText.find('臺北市立') != -1):
                        for item in allText.split(' '):
                            if(item.find('臺北市立') != -1):
                                school = item.split('　')[0]
                                break

                        # 基本資料
                        basicTable = page.extract_tables()[0][0]
                        name = basicTable[3]
                        # 成績
                        scoreTable = page.extract_tables()[1]
                        # 全校
                        schoolScore = scoreTable[len(scoreTable)-1]
                        # 個人
                        personScore = scoreTable[len(scoreTable)-2]

                        for i in range(5):
                            score[0 + 3 *
                                  i] = round(float(personScore[5 + (i*7)]), 2)
                            score[1 + 3 *
                                  i] = round(float(personScore[6 + (i*7)]), 2)
                            score[2 + 3 *
                                  i] = round(float(personScore[7 + (i*7)]), 2)
                    # 新北市市立高中 Layout
                    elif(allText.find('新北市市立') != -1):
                        school = allText.split(' ')[0]
                        for item in allText.split(' '):
                            if(item.find('姓名') != -1):
                                name = item.split('：')[1]
                                break
                        # 只有一張Table
                        tableLen = len(page.extract_tables()[0])
                        # 成績橫向格數
                        scoreLocation = [2, 4, 6, 8, 10]
                        for i in range(5):
                            score[0 + 3 * i] = round(
                                float(page.extract_tables()[0][tableLen-5][scoreLocation[i]]))
                            score[1 + 3 * i] = round(
                                float(page.extract_tables()[0][tableLen-3][scoreLocation[i]]))
                            score[2 + 3 * i] = round(
                                float(page.extract_tables()[0][tableLen-1][scoreLocation[i]]))
                    # 國立 Layout & 桃園市立 Layout & 高雄市立 Layout
                    elif(allText.find('國立') != -1 or allText.find('高雄市立') != -1 or allText.find('桃園市立') != -1):
                        if(allText.find('國立') != -1):
                            school = allText[allText.index('國立'):allText.index('學')+1]
                        elif(allText.find('高雄市立') != -1):
                            school = allText[allText.index('高雄市立'):allText.index('學')+1]
                        elif(allText.find('桃園市立') != -1):
                            school = allText[allText.index('桃園市立'):allText.index('學')+1]

                        for item in allText.split(' '):
                            if(item.find('姓名') != -1):
                                name = item.split('：')[1]
                                break
                        # 只有一張Table
                        tableLen = len(page.extract_tables()[0])
                        # 成績橫向格數
                        scoreLocation = [1, 3, 5, 7, 9]
                        for i in range(5):
                            # sample: 10/30
                            classScore = page.extract_tables()[0][tableLen-4][scoreLocation[i]]
                            categoryScore = page.extract_tables()[0][tableLen-3][scoreLocation[i]]
                            allScore = page.extract_tables()[0][tableLen-2][scoreLocation[i]]
                            if(school == '國立內壢高級中學'):
                                # 跑版
                                # 相除後無條件進位
                                # 其中一項為0,欄位帶入0
                                if(float(categoryScore.split('\n')[0].split('/')[0]) == 0 or float(categoryScore.split('\n')[0].split('/')[1]) ==0):
                                    score[0 + 3 * i] = '0'
                                else:
                                    score[0 + 3 * i] = math.ceil((float(categoryScore.split('\n')[0].split('/')[0])/float(categoryScore.split('\n')[0].split('/')[1]))*100)
                                if(float(categoryScore.split('\n')[1].split('/')[0]) == 0 or float(categoryScore.split('\n')[1].split('/')[1]) == 0):
                                    score[1 + 3 * i] = '0'
                                else:
                                    score[1 + 3 * i] = math.ceil((float(categoryScore.split('\n')[1].split('/')[0])/float(categoryScore.split('\n')[1].split('/')[1]))*100)
                                if(float(allScore.split('/')[0]) == 0 or float(allScore.split('/')[1]) == 0):
                                    score[2 + 3 * i] = '0'
                                else:
                                    score[2 + 3 * i] = math.ceil((float(allScore.split('/')[0])/float(allScore.split('/')[1]))*100)
                            else: 
                                # 相除後無條件進位
                                # 其中一項為0,欄位帶入0
                                if(float(classScore.split('/')[0]) == 0 or float(classScore.split('/')[1]) == 0):
                                    score[0 + 3 * i] = '0'
                                else:
                                    score[0 + 3 * i] = math.ceil((float(classScore.split('/')[0])/float(classScore.split('/')[1]))*100)
                                if(float(categoryScore.split('/')[0]) == 0 or float(categoryScore.split('/')[1]) == 0):
                                    score[1 + 3 * i] = '0'
                                else:
                                    score[1 + 3 * i] = math.ceil((float(categoryScore.split('/')[0])/float(categoryScore.split('/')[1]))*100)
                                if(float(allScore.split('/')[0]) == 0 or float(allScore.split('/')[1]) == 0):
                                    score[2 + 3 * i] = '0'
                                else:
                                    score[2 + 3 * i] = math.ceil((float(allScore.split('/')[0])/float(allScore.split('/')[1]))*100)
                    else:
                        isOk = False
                        message = '該學生所屬高中並未設定Layout!'
                    break
        # 找不到需要資料的情況
        if(isOk == True and name == ''):
            isOk = False
            message = '找不到該學生之成績單頁面!'

    except Exception as e:
        isOk = False
        message = sysException(e)
    finally:
        pdf.close()

    return basicModel(id, school, name, isOk=isOk, message=message), scoreModel(score)
