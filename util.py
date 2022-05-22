import re

def fullCasePath(x):
  return 'input/' + x + '.in'

def formatCaseNumber(x):
  if x < 10:
    return "00" + str(x)
  elif x < 100:
    return "0" + str(x)
  return str(x)
  
def formatGroupNumber(x):
  return '%d' % x
  
def isHiddenFile(filename):
  return re.match('^\.', filename) != None

