import sys
import traceback

from root import root
from sysException import sysException

# Data path
# path = '備審資料'
# Test path
path = '備審資料/106生醫/10117018'

try:
    
    if __name__ == '__main__':
        # 1: use layout.txt setting to get score and append excel
        # 2: print pdf score page data
        # 3: test pdf setting with layout.txt

        print("--------------------------------------------------------------")
        # root(path,1)
        print("--------------------------------------------------------------")
        root(path,2)
        print("--------------------------------------------------------------")
        # root(path,3)
        print("--------------------------------------------------------------")

except Exception as e:
    print(sysException(e))