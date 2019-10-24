import sys
import traceback

from root import root
from sysException import sysException

# custom exception
class customException(Exception):
    pass

# Data path
path = './備審資料/106生醫'
# Test path
# path = './test'

try:
    if __name__ == '__main__':
        root(path)
except Exception as e:
    print(sysException(e))