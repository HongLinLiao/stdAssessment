# basic model
class BasicModel():
    def __init__(self, id, name, isOk = True, message = ''):
        # 流水序號
        self.id = id
        # 學生姓名
        self.name = name
        # 是否成功
        self.isOk = isOk
        # 訊息
        self.message = message

        
# score model
class ScoreModel():
    def __init__(self, score):

        # 依序為班級排名百分比、類組排名百分比、年級排名百分比

        # 高一上學期 
        self.firstＵpClassPercentage = score[0]
        self.firstUpCategoryPercentage = score[1]
        self.firstUpAllPercentage = score[2]

        # 高一下學期
        self.firstDownClassPercentage = score[3]
        self.firstDownCategoryPercentage = score[4]
        self.firstDownAllPercentage = score[5]

        # 高二上學期
        self.secondＵpClassPercentage = score[6]
        self.secondUpCategoryPercentage = score[7]
        self.secondUpAllPercentage = score[8]

        # 高二下學期
        self.secondDownClassPercentage = score[9]
        self.secondDownCategoryPercentage = score[10]
        self.secondDownAllPercentage = score[11]

        # 高三上學期
        self.thirdＵpClassPercentage = score[12]
        self.thirdUpCategoryPercentage = score[13]
        self.thirdUpAllPercentage = score[14]

