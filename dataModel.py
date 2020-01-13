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
        #department
        self.department = department
        # school name
        self.school = school
        # student name
        self.name = name
        # score data
        self.data = data

        
# score model
class ScoreModel():

    # 高一
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

    # 高二
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

    # 高三
    thirdUpClassRank = ''
    thirdUpClassCount = ''
    thirdUpClassPercentage = ''
    thirdUpCategoryRank = ''
    thirdUpCategoryCount = ''
    thirdUpCategoryPercentage = ''
    thirdUpAllRank = ''
    thirdUpAllCount = ''
    thirdUpAllPercentage = ''

    def __init__(self):
        pass

