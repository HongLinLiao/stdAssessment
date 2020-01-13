# pip install pdfplumber
import pdfplumber
import math
from enum import Enum
import re
import numpy as np

from dataModel import ReturnModel as returnModel
from dataModel import BasicModel as basicModel
from dataModel import ScoreModel as scoreModel
from sysException import sysException

#region Foundation Setting

# get pdf layout setting
def getLayoutSetting():
    fileLine = open('layout.txt','r').readlines()

    layoutSettings = []
    layoutObj = {}

    # data group
    forGroup = 8
    group = 1

    # attribute count
    forCount = 10 
    count = 1

    semester = ''
    line = ''

    for line in fileLine:
        if(line.strip() != '' and line.find('=')==-1):

            if(group == 1):

                tempArray = []
                for item in range(len(line.strip().split(','))):
                    if(item ==0):
                        layoutObj['year'] = line.strip().split(',')[item]
                    else:
                        tempArray.append(line.strip().split(',')[item])
                
                layoutObj['school'] = tempArray
                group = group +1

            elif(group ==2):

                # Hardcode name attribute
                setting = handleLayoutValue(line.strip().split(':')[1])
                if(setting == 'null'):
                    layoutObj['nameTable'] = None
                    layoutObj['nameRow'] = None
                    layoutObj['nameIndex'] = None
                else:
                    layoutObj['nameTable'] = setting[0]
                    layoutObj['nameRow'] = setting[1]
                    layoutObj['nameIndex'] = setting[2]

                group = group +1
            
            else:

                if(count == 1):
                    semester = line
                    count = count + 1
                else:
                    variableName = getVariableName(semester, line)

                    setting = handleLayoutValue(line.strip().split(':')[1])
                    layoutObj[variableName+'Table'] = setting[0]
                    layoutObj[variableName+'Row'] = setting[1]
                    layoutObj[variableName+'Index'] = setting[2]
                    
                    if(count+1 > forCount):
                        count = 1
                        group = group +1
                    else:
                        count = count + 1

            if(group+1>forGroup+1):
                group = 1
                layoutSettings.append(layoutObj)
                layoutObj = {}

    return layoutSettings

# get variable name
def getVariableName(semester, item):

    variableName = ''

    # year
    if(semester.find('高一') != -1):
        variableName = variableName + 'first'
    elif(semester.find('高二') != -1):
        variableName = variableName + 'second'
    elif(semester.find('高三') != -1):
        variableName = variableName + 'third'
    elif(semester.find('總學年') != -1):
        variableName = variableName + 'whole'

    # semester
    if(semester.find('上學期') != -1):
        variableName = variableName + 'Up'
    elif(semester.find('下學期') != -1):
        variableName = variableName + 'Down'

    # category
    if(item.find('班級') != -1):
        variableName = variableName + 'Class'
    elif(item.find('類組') != -1):
        variableName = variableName + 'Category'
    elif(item.find('年級') != -1):
        variableName = variableName + 'All'

    # item
    if(item.find('排名百分比') != -1):
        variableName = variableName + 'Percentage'
    elif(item.find('排名') != -1):
        variableName = variableName + 'Rank'
    elif(item.find('總人數') != -1):
        variableName = variableName + 'Count'

    return variableName

# deal layout table(string)
def handleLayoutValue(text):
    array = []

    table = text.split(',')[0]

    if(table != 'null'):
        if(table != 'None'):
            array.append(int(table));
            row = int(text.split(',')[1].split('-')[1])
            row = row + 1
            array.append(row)
            index = int(text.split(',')[2])
            array.append(index)
        else:
            array.append(None)
            array.append(None)
            index = int(text.split(',')[2])
            array.append(index)
    else:
        array.append(None)
        array.append(None)
        array.append(None)

    return array

# deal school name rule
def handleSchoolName(allText, schoolSetting):

    schoolNameStartIndex = allText.find(schoolSetting)
    
    # decide what word is end in school name
    schoolNameEndIndex = 0

    schoolKeyWord = ['學校','高中','中學','女中']

    for keyWord in schoolKeyWord :

        if(allText.find(keyWord) != -1):
            allIndex = [m.start() for m in re.finditer(keyWord, allText)]

            for index in allIndex:
                if(index<=schoolNameStartIndex):
                    continue
                else:
                    if(schoolNameEndIndex == 0 or index < schoolNameEndIndex):
                        schoolNameEndIndex = index + len(keyWord)
                    break
    
    returnSetting = ['高中','附中','高商','壢中']
    returnState = False
    for item in returnSetting:
        if(schoolSetting.find(item)!= -1):
            returnState = True
            break

    if(returnState == True):
        return schoolSetting
    elif(schoolNameEndIndex == 0):
        return '找不到學校結尾字元'
    else:
        return allText[schoolNameStartIndex:schoolNameEndIndex]

# deal student name rule
def handleStudentName(layout, page, allText):

    table = layout['nameTable']
    row = layout['nameRow']
    index = layout['nameIndex']

    if(table is not None):
        row = len(page[table])-row
        return page[table][row][index]
    else:
        allText = allText.replace(' ','')

        name = ''
        nameLabel = 0

        if(allText.find("姓名：") != -1):
            nameLabel = allText.find("姓名：")
        elif(allText.find("學生：") != -1):
            nameLabel = allText.find("學生：")

        name = allText[nameLabel+3:nameLabel+6]

        if(len(name)>=5):
            return "姓名讀取錯誤！"
        else:
            return name 

# search correct score page from all text
def getCorrectScorePage(allText):

    text = allText.replace(" ", "")
    target = ['成績證明書','成績證明單','個人成績單','個人成績暨分數百分比','學業成績','學生成績表','成績一覽表'
    ] 

    for item in target:
         if(text.find(item) != -1):

             return True

    return False

# search correct layout from all layouts
def getCorrectLayout(allText, layoutSettings, targetYear):

    # rule: if u customize a school, u will customize until end
    array = []

    for layout in layoutSettings:
        if(int(layout['year']) > int(targetYear)):
            continue
        else:
            # from school array find correct school
            for school in layout['school']:
                if(allText.find(school) != -1):
                    layout['schoolName'] = school
                    array.append(layout)

    target = {}

    if(len(array)>0):
        for i in range(len(array)):
            if(i == 0):
                target = array[i]
            else:
                if(len(array[i]['schoolName']) >= len(target['schoolName'])):
                    if(int(array[i]['year']) >= int(target['year'])):
                        target = array[i]                    

        return returnModel(data = target) 
    else:
        return returnModel(isOk=False, message='找不到Layout!')

# No Table Layout()
def noTableLayout(allText, layout, scoreModel, printTest):

    returnResult = returnModel()

    state = False

    for scoreRow in allText.split('\n'):
        
        # print(scoreRow)
        if(scoreRow.find("學科平均") != -1 or scoreRow.find("智育成績") != -1 or scoreRow.find("學業平均") != -1 or scoreRow.find("學業成績") != -1):

            state = True

            scoreArray = np.array(scoreRow.split(' '))

            removeIndex = []

            for i in range(len(scoreArray)):
                if(len(scoreArray[i]) == 0):
                    removeIndex.append(i)

            scoreArray = np.delete(scoreArray, removeIndex)

            # print(scoreArray)

            # score data
            for attribute in attributes:

                variableName = getVariableName(attribute.split(',')[0], attribute.split(',')[1])

                if(layout[variableName+'Index'] != None):
                    
                    score = scoreArray[layout[variableName+'Index']]

                    if(printTest == False):
                        setattr(scoreModel, variableName, score)
                    else:
                        print("%s: %s"%(attribute, score))
            
            returnResult.isOk = True
            returnResult.message = ''
            returnResult.data = scoreModel
        
            break

    if(state == False):
        # Test Print
        if(printTest):
            print("成績列不對或不適用No Table Layout!")

        returnResult.message = "成績列不對或不適用No Table Layout!"

    return returnResult

# what attributes u want to get from score page
attributes = [
    "高一上學期,班級排名",
    "高一上學期,班級總人數",
    "高一上學期,班級排名百分比",
    "高一上學期,類組排名",
    "高一上學期,類組總人數",
    "高一上學期,類組排名百分比",
    "高一上學期,年級排名",
    "高一上學期,年級總人數",
    "高一上學期,年級排名百分比",
    "高一下學期,班級排名",
    "高一下學期,班級總人數",
    "高一下學期,班級排名百分比",
    "高一下學期,類組排名",
    "高一下學期,類組總人數",
    "高一下學期,類組排名百分比",
    "高一下學期,年級排名",
    "高一下學期,年級總人數",
    "高一下學期,年級排名百分比",

    "高二上學期,班級排名",
    "高二上學期,班級總人數",
    "高二上學期,班級排名百分比",
    "高二上學期,類組排名",
    "高二上學期,類組總人數",
    "高二上學期,類組排名百分比",
    "高二上學期,年級排名",
    "高二上學期,年級總人數",
    "高二上學期,年級排名百分比",
    "高二下學期,班級排名",
    "高二下學期,班級總人數",
    "高二下學期,班級排名百分比",
    "高二下學期,類組排名",
    "高二下學期,類組總人數",
    "高二下學期,類組排名百分比",
    "高二下學期,年級排名",
    "高二下學期,年級總人數",
    "高二下學期,年級排名百分比",

    "高三上學期,班級排名",
    "高三上學期,班級總人數",
    "高三上學期,班級排名百分比",
    "高三上學期,類組排名",
    "高三上學期,類組總人數",
    "高三上學期,類組排名百分比",
    "高三上學期,年級排名",
    "高三上學期,年級總人數",
    "高三上學期,年級排名百分比",

    "總學年,班級排名",
    "總學年,班級總人數",
    "總學年,班級排名百分比",
    "總學年,類組排名",
    "總學年,類組總人數",
    "總學年,類組排名百分比",
    "總學年,年級排名",
    "總學年,年級總人數",
    "總學年,年級排名百分比",
]

#endregion

# print pdf table to find layout for setting txt
def findPdfLayout(path):
    try:
        print(path)

        scorePageState = False

        pdf = pdfplumber.open(path)

        for page in pdf.pages:

            # get page all text
            allText = page.extract_text()

            print(allText)

            if(isinstance(allText, str)):
                # find score page
                if(getCorrectScorePage(allText)):

                    scorePageState = True
                    
                    # Current Table
                    tableCounter = 0

                    print("Table Length: %s" % (len(page.extract_tables())))

                    for tableCount in range(len(page.extract_tables())):
                        print("Table: %s"%(tableCount))
                        print(page.extract_tables()[tableCount])
                        print("=================================================")

                    break
        
        if(scorePageState == False):
            print('找不到成績單頁面！')

    except Exception as e:
        message = sysException(e)
    finally:
        pdf.close()

# test pdf layout setting
def testPdfLayout(path, layoutSettings):

    try:

        # pdf year(Hardcode)
        targetYear = path.split('/')[len(path.split('/'))-3][0:3]

        pdf = pdfplumber.open(path)

        for page in pdf.pages:

            # get page all text
            allText = page.extract_text()

            if(isinstance(allText, str)):

                # find score page
                if(getCorrectScorePage(allText)):

                    print("Search Layout......")
                    layoutResult = getCorrectLayout(allText, layoutSettings, targetYear)
                    print("Search Layout Complete!")

                    if(layoutResult.isOk):

                        # year
                        year = layoutResult.data['year']
                        
                        # school name
                        schoolName = handleSchoolName(allText, layoutResult.data['schoolName'])

                        # student name (hardcode)
                        studentName = handleStudentName(layoutResult.data, page.extract_tables(), allText)

                        print("使用%s學年度Layout,%s,%s"%(year, schoolName, studentName))

                        noTableState = True

                        # score data
                        for attribute in attributes:

                            variableName = getVariableName(attribute.split(',')[0], attribute.split(',')[1])

                            table = layoutResult.data[variableName+'Table']
                            row = layoutResult.data[variableName+'Row']
                            index = layoutResult.data[variableName+'Index']

                            score = ''
                            if(table is not None):
                                row = len(page.extract_tables()[table])-row
                                score = page.extract_tables()[table][row][index]

                            # %
                            score = score.replace("%","")
                            # %
                            score = score.replace("％","")
                            # whitespace
                            score = score.replace(" ","")

                            # example: 18/34  
                            if(score.find('/') != -1):
                                if(variableName.find('Rank') != -1):
                                    score = score.split("/")[0]
                                elif(variableName.find('Count') != -1):
                                    score = score.split("/")[1]
                            
                            if(score.find("／") != -1):
                                if(variableName.find('Rank') != -1):
                                    score = score.split("／")[0]
                                elif(variableName.find('Count') != -1):
                                    score = score.split("／")[1]
                            
                            if(score != ''):
                                noTableState = False
                                print("%s: %s"%(attribute, score))

                        if(noTableState):

                            print("Test No Table Layout")
                            
                            noTableLayout(allText, layoutResult.data, None, True)

                    else:
                        print(layoutResult.message)

                    break

    except Exception as e:
        message = sysException(e)
    finally:
        pdf.close()

# get score data
def getScoreData(layout, page, scoreResult):

    returnResult = returnModel()

    noTableState = True

    # score data
    for attribute in attributes:

        variableName = getVariableName(attribute.split(',')[0], attribute.split(',')[1])

        table = layout[variableName+'Table']
        row = layout[variableName+'Row']
        index = layout[variableName+'Index']

        score = ''

        if(table is not None):
            row = len(page[table])-row
            score = page[table][row][index]

        # %
        score = score.replace("%","")
        # %
        score = score.replace("％","")
        # whitespace
        score = score.replace(" ","")

        # example: 18/34  
        if(score.find('/') != -1):
            if(variableName.find('Rank') != -1):
                score = score.split("/")[0]
            elif(variableName.find('Count') != -1):
                score = score.split("/")[1]

        # example: 18／34  
        if(score.find("／") != -1):
            if(variableName.find('Rank') != -1):
                score = score.split("／")[0]
            elif(variableName.find('Count') != -1):
                score = score.split("／")[1]

        setattr(scoreResult, variableName, score)

        if(score != ''):
            noTableState = False
    
    if(noTableState):
        returnResult.isOk = False
    else:
        returnResult.isOk = True
    
    returnResult.data = scoreResult

    return returnResult

# get all data
def convertInfo(path, layoutSettings):
    
    # ReturnModel
    isOk = True
    message = ''

    # BasicModel
    id = ''
    school = ''
    name = ''
    targetYear = path.split('/')[len(path.split('/'))-3][0:3]
    department = path.split('/')[len(path.split('/'))-3][3:len(path.split('/')[len(path.split('/'))-3])]

    # ScoreModel
    scoreResult = scoreModel()

    try:
        # pdf year(Hardcode)
        targetYear = path.split('/')[len(path.split('/'))-3][0:3]

        id = path.split('/')[len(path.split('/'))-1].split('.')[0]

        # print("ID: %s, Process..."%(id))

        pdf = pdfplumber.open(path)

        for page in pdf.pages:

            # get page all text
            allText = page.extract_text()

            if(isinstance(allText, str)):

                # find score page
                if(getCorrectScorePage(allText)):

                    # print("Search Layout......")
                    layoutResult = getCorrectLayout(allText, layoutSettings, targetYear)
                    # print("Search Layout Complete!")

                    if(layoutResult.isOk):

                        # basic data
                        # print("Basic Loading......")

                        # school name
                        school = handleSchoolName(allText, layoutResult.data['schoolName'])

                        # student name (hardcode)
                        name = handleStudentName(layoutResult.data, page.extract_tables(), allText)

                        # print("%s,%s"%(school, name))

                        # print("Basic Loading Complete!")

                        # score data
                        # print("Score Loading......")

                        scoreReturn = getScoreData(layoutResult.data, page.extract_tables(), scoreResult)

                        scoreResult = scoreReturn.data

                        if(scoreReturn.isOk == False):
                            scoreReturn = noTableLayout(allText, layoutResult.data, scoreResult, False)
    
                            if(scoreReturn.isOk):
                                scoreResult = scoreReturn.data
                            else:
                                isOk = scoreReturn.isOk
                                message = scoreReturn.message

                        # print("Score Loading Complete!")
                    else:
                        isOk = False
                        message = '找不到Layout！'

                    break

        if(isOk and school=='' and message==''):
            isOk = False
            message = '找不到成績單頁面！'

    except Exception as e:

        isOk = False
        message = sysException(e)

    finally:
        pdf.close()

    return returnModel(
        isOk=isOk,
        message=message,
        data=basicModel(
            id,
            targetYear,
            department,
            school,
            name,
            data= scoreResult
        )
    )

   