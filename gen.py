import sys, os

splitLine = "===================="
caseCount = 0
curCase = None

def fmtCaseNum(x):
  if x < 10:
    return "00" + str(x)
  elif x < 100:
    return "0" + str(x)
  return str(x)

def newCase():
  global caseCount, curCase
  filename = "input/input" + fmtCaseNum(caseCount) + ".txt"
  curCase = open(filename, "w")

def closeCase():
  global curCase, caseCount
  if not curCase is None:
    curCase.close()
    curCase = None
    print "Done case %d" % caseCount
    caseCount = caseCount + 1
  else:
    print >> sys.stderr, "No file was open, but splitLine was found."
    
def parseRule(ruleFile):
  f = open(ruleFile, "r")
  rules = []
  while True:
    line = f.readline()
    if not line: break
      
    tokens = line.rstrip().replace(" ", "").split("=")
    op = tokens[0]
    if op == "": continue
    assert op == "group", "Missing 'group' operator"
    
    group = {
      "name": tokens[1]
    }
    while True:
      gline = f.readline()
      assert gline, "group def not complete"
      gtokens = gline.rstrip().replace(" ", "").split("=")
      gop = gtokens[0]
      
      if gop == "func":
        group['func'] = gtokens[1]
      elif gop == "num":
        group['num'] = int(gtokens[1])
      elif gop == "end":
        rules.append(group)
        break
      elif gop == "param":
        # parse parameters
        param = []
        for i in range(group['num']):
          pline = f.readline()
          assert pline, "param def not complete"
          pline = pline.rstrip().replace(" ", "")
          if pline == "...":
            assert i > 0, "No param to repeat"
            for j in range(i, group['num']):
              param.append(param[i - 1])
            break
          passigns = pline.split(",")
          paras = {}
          for j in range(len(passigns)):
            assign = passigns[j].split("=")
            para, val = assign[0], assign[1]
            paras[para] = val
          param.append(paras)
        group['param'] = param
  return rules
      
def init():
  global caseCount, curCase
  # create an input folder
  if not os.path.exists("input"):
    os.makedirs("input")
  curCase = None
  caseCount = 0
    
def manualCases(directory):    
  # copy all the manual tests
  for dirname, dirnames, filenames in os.walk(directory):
    for filename in filenames:
      with open(directory + "/" + filename, "r") as f:
        for line in f:
          line = line.rstrip()
          tokens = line.split(" ")
          if tokens[0] == splitLine:
            closeCase()
          else: # not a split line
            if curCase is None:
              newCase()
            curCase.write(line + "\n")
        # close the last case
        if not curCase is None:
          closeCase()
          
def programCases(rules, input_package):
  # TODO for each rule, call
  for rule in rules:
    func = getattr(input_package, rule['func'])
    num = rule['num']
    for i in range(num):
      if not 'param' in rule:
        params = {}
      else:
        params = rule['param'][i]
      res = func(params)
      newCase()
      curCase.write(res)
      closeCase()
      