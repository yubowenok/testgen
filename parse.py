import re

SPLIT_LINE = '===================='

def parseSplitLine(line):
  tokens = re.split('\s+', line.rstrip())
  
  if tokens[0] != SPLIT_LINE:
    return {'isSplitLine': False}
  
  result = {'isSplitLine': True}
  for x in tokens[1:]:
    set_name = re.match('^name:(.*)', x)
    if set_name != None:
      result['name'] = set_name.group(1)
  return result
  

def parseRules(rule_file):
  f = open(rule_file, 'r')
  rules, lines = [], []
  f_lines = f.readlines()
  
  for line in f_lines:
    line = line.rstrip()
    non_comment = re.match('^(.*)#.*$', line)
    if non_comment != None:
      line = non_comment.group(1)
    if line == '':
      continue
    lines.append(line)
  
  line_counter = 0
  while line_counter < len(lines):
    line = lines[line_counter]
    tokens = line.replace(' ', '').split('=')
    
    op = tokens[0]
    if op == '': continue
    assert op == 'group', 'missing "group" operator'
    
    group = {
      'name': tokens[1]
    }
    while True:
      gline = lines[line_counter]
      line_counter += 1
      
      assert gline, 'group def not complete'
      gtokens = gline.replace(' ', '').split('=')
      gop = gtokens[0]
      
      if gop == 'func':
        group['func'] = gtokens[1]
      elif gop == 'num':
        group['num'] = int(gtokens[1])
      elif gop == 'end':
        rules.append(group)
        break
      elif gop == 'param':
        # parse parameters
        param = []
        for i in range(group['num']):
          pline = lines[line_counter]
          line_counter += 1
          
          assert pline, 'param def not complete'
          pline = pline.replace(' ', '')
          if pline == '...':
            assert i > 0, 'No param to repeat'
            for j in range(i, group['num']):
              param.append(param[i - 1])
            break
          passigns = pline.split(',')
          paras = {}
          for j in range(len(passigns)):
            assign = passigns[j].split('=')
            para, val = assign[0], assign[1]
            paras[para] = val
          param.append(paras)
        group['param'] = param
  return rules
  

def parseGroups(group_file):
  f = open(group_file, 'r')
  lines = [line.rstrip() for line in f.readlines() if line.rstrip() != '']
  
  groups = []
  file_counter = 0
  
  for line in lines:
    file_count = re.match('^(\d+).*', line) 
    if file_count == None: # ignore lines with no file counts
      continue
    
    no_groups = re.match('^none.*', line)  
    if no_groups != None:
      break

    tokens = re.split('\s+', line)
    group = {}
    group['file_count'] = int(tokens[0])
    
    other_tokens = tokens[1:]
    if len(other_tokens) > 0 and other_tokens[0] != '#':
      raise Exception('expecting comments or EOL, but got something else')
    for token in other_tokens:
      set_name = re.match('^name:(.*)', token)
      if set_name != None:
        group['name'] = set_name.group(1)
    
    groups.append(group)
  return groups
