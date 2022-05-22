import os, sys, shutil
from subprocess import call

from .util import formatCaseNumber, formatGroupNumber, fullCasePath, isHiddenFile
from .parse import parseSplitLine, parseRules, parseGroups

class Problem:
  def __init__(self, problem_id):
    # create/clear the input/output folder
    if os.path.exists('input'):
      shutil.rmtree('input')
    os.makedirs('input')
    if os.path.exists('output'):
      shutil.rmtree('output')
    os.makedirs('output')
    
    self.cur_case_file = None
    self.case_count = 0
    self.problem_id = problem_id
    
  def newCase(self):
    self.case_count += 1
    self.cur_case_name = formatCaseNumber(self.case_count)
    filename = fullCasePath(self.cur_case_name)
    self.cur_case_file = open(filename, 'w')
    
  def closeCase(self, name=None, group_num=None):
    if self.cur_case_file is None:
      raise Exception('no case was open, but split line was found to close')
    self.cur_case_file.close()
    self.cur_case_file = None
    
    new_case_name = self.cur_case_name
    if name != None:
      new_case_name += '-' + name
    if group_num != None:
      new_case_name += '-%s' % formatGroupNumber(group_num)
      
    if new_case_name != self.cur_case_name:
      os.rename(fullCasePath(self.cur_case_name), fullCasePath(new_case_name))
      self.cur_case_name = new_case_name
    
    print ('Done case %s' % self.cur_case_name)
 
  def manualCases(self, directory):    
    # copy all the manual tests
    for dirname, dirnames, filenames in os.walk(directory):
      for filename in sorted(filenames):
        if isHiddenFile(filename): # skip hidden files
          continue
        with open(directory + '/' + filename, 'r') as f:
          for line in f:
            line = line.rstrip()
            split_line_info = parseSplitLine(line)
            
            if split_line_info['isSplitLine']:
              case_name = split_line_info['name'] if 'name' in split_line_info else None
              self.closeCase(name=case_name)
            else: # not a split line
              if self.cur_case_file is None:
                self.newCase()
              self.cur_case_file.write(line + '\n')
          # close the last case
          if not self.cur_case_file is None:
            self.closeCase()
            
  def programCases(self, rule_file, input_package):
    rules = parseRules(rule_file)
    for rule in rules:
      func = getattr(input_package, rule['func'])
      num = rule['num']
      group_num = 0
      for i in range(num):
        if not 'param' in rule:
          params = {}
        else:
          params = rule['param'][i]
        res = func(params)
        self.newCase()
        self.cur_case_file.write(res)
        group_num += 1
        self.closeCase(name=rule['name'], group_num=group_num if num > 1 else None)

  def packCases(self, group_file):
    groups = parseGroups(group_file)
    if len(groups) == 0:
      print ('no case packing required', file=sys.stderr)
      return
    
    def getNextTmpFilename(file_number, name=None):
      res = ''
      file_name = str(file_number)
      if name != None:
        file_name += '-' + name
      if file_number < 10:
        res = '00' + file_name + '.tmp'
      elif file_number < 100:
        res = '0' + file_name + '.tmp'
      return res
  
    for dirname, dirnames, filenames in os.walk('input'):
      filenames = [filename for filename in sorted(filenames) if not isHiddenFile(filename)]
      counter = 0
      for group_index, group in enumerate(groups):
        new_filepath = os.path.join(dirname, 
            getNextTmpFilename(group_index + 1, name=group['name'] if 'name' in group else None))
        out_file = open(new_filepath, 'w')
        contents = ''
        for i in range(counter, counter + group['file_count']):
          if i >= len(filenames):
            raise Exception('not enough input files')
          filepath = os.path.join(dirname, filenames[i])
          file = open(filepath, 'r')
          lines = file.readlines()
          file.close()
          contents += ''.join(lines)
        
        out_file.write(str(group['file_count']) + '\n') # prepend number of cases
        out_file.write(contents)
        out_file.close()
        
        counter += group['file_count']
      
      if counter < len(filenames):
        print ('Warning: not all input files were used', file=sys.stderr)
  
    # delete all single-case input files
    for dirname, dirnames, filenames in os.walk('input'):
      for filename in filenames:
        if filename[-3:] == '.in':
          filepath = os.path.join(dirname, filename)
          os.remove(filepath)
    
    # rename tmp files to new input files
    for filename in filenames:
      if filename[-4:] == '.tmp':
        new_filename = filename[:-4] + '.in'
        filepath = os.path.join(dirname, filename)
        new_filepath = os.path.join(dirname, new_filename)
        os.rename(filepath, new_filepath)
        
  def generateAnswers(self, solution_source):
    # a wrapper around test_runner
    call([os.path.join(os.path.dirname(__file__), 'test_runner.sh'), 'run', solution_source])
