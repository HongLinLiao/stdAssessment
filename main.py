import sys
import traceback

from root import root
from sysException import sysException

# custom exception
class customException(Exception):
    pass

path = './備審資料/106生醫'
# path = './test'

try:
    if __name__ == '__main__':
        root(path)
except Exception as e:
    print(sysException(e))