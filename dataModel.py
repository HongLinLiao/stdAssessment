# state model
class ReturnModel():
    def __init__(self, isOk = True, message = '', data = None):

        self.isOk = isOk
        self.message = message
        self.data = data

# basic model
class BasicModel():
    def __init__(self, id, year, department, school, name, data = None):

        # pdf file id
        self.id = id
        # year
        self.year = year
        # department
        self.department = department
        # school name
        self.school = school
        # student name
        self.name = name
        # score data
        self.data = data

        
# score model
class ScoreModel():

    # first: 高一
    # second: 高二
    # third: 高三
    # whole: 總學年

    # Up: 上學期
    # Down: 下學期

    # Class: 班級
    # Category: 類組
    # All: 年級

    # Rank: 排名
    # Count: 人數
    # Percentage: 排名百分比

    firstUpClassRank = ''
    firstUpClassCount = ''
    firstUpClassPercentage = ''
    firstUpCategoryRank = ''
    firstUpCategoryCount = ''
    firstUpCategoryPercentage = ''
    firstUpAllRank = ''
    firstUpAllCount = ''
    firstUpAllPercentage = ''
    firstDownClassRank = ''
    firstDownClassCount = ''
    firstDownClassPercentage = ''
    firstDownCategoryRank = ''
    firstDownCategoryCount = ''
    firstDownCategoryPercentage = ''
    firstDownAllRank = ''
    firstDownAllCount = ''
    firstDownAllPercentage = ''

    secondUpClassRank = ''
    secondUpClassCount = ''
    secondUpClassPercentage = ''
    secondUpCategoryRank = ''
    secondUpCategoryCount = ''
    secondUpCategoryPercentage = ''
    secondUpAllRank = ''
    secondUpAllCount = ''
    secondUpAllPercentage = ''
    secondDownClassRank = ''
    secondDownClassCount = ''
    secondDownClassPercentage = ''
    secondDownCategoryRank = ''
    secondDownCategoryCount = ''
    secondDownCategoryPercentage = ''
    secondDownAllRank = ''
    secondDownAllCount = ''
    secondDownAllPercentage = ''

    thirdUpClassRank = ''
    thirdUpClassCount = ''
    thirdUpClassPercentage = ''
    thirdUpCategoryRank = ''
    thirdUpCategoryCount = ''
    thirdUpCategoryPercentage = ''
    thirdUpAllRank = ''
    thirdUpAllCount = ''
    thirdUpAllPercentage = ''

    wholeClassRank = ''
    wholeClassCount = ''
    wholeClassPercentage = ''
    wholeCategoryRank = ''
    wholeCategoryCount = ''
    wholeCategoryPercentage = ''
    wholeAllRank = ''
    wholeAllCount = ''
    wholeAllPercentage = ''

    def __init__(self):
        pass

