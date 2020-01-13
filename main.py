import sys
import traceback

from root import root
from sysException import sysException

# custom exception
class customException(Exception):
    pass

# Data path
path = '備審資料'
# Test pathç
# path = '備審資料/108資管/10330004'

try:
    
    if __name__ == '__main__':
        # 1: use txt setting to find score and append excel
        # 2: print pdf score page data
        # 3: test pdf setting

        print("--------------------------------------------------------------")
        root(path,1)
        print("--------------------------------------------------------------")
        # root(path,2)
        print("--------------------------------------------------------------")
        # root(path,3)
        print("--------------------------------------------------------------")

except Exception as e:
    print(sysException(e))