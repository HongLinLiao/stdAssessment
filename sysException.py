import sys
import traceback

# return system exception info
def sysException(e:Exception):
    error_class = e.__class__.__name__ # error type
    detail = e.args[0] # error details
    cl, exc, tb = sys.exc_info() # get Call Stack
    lastCallStack = traceback.extract_tb(tb)[-1] # Call Stack last data 
    fileName = lastCallStack[0] # error file name
    lineNum = lastCallStack[1] # error location
    funcName = lastCallStack[2] # error function 
    errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
    return errMsg
