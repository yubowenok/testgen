import sys

# add testgen to system path, or include the path here
sys.path.append('../..')

from testgen import Problem
import funcs

# create a new problem instance with given id
prob = Problem('aplusb')

# copy from the manual cases in input_manual
prob.manualCases('input_manual')

# parse the test generator rules defined in the file "aplusb.rules",
# and generate tests via program using the rules
prob.programCases('aplusb.rules', funcs)

# group the cases into smaller number of files
# to create multpile subtasks or be compatible with non single-case judges
prob.packCases('aplusb.groups')

# generate answers using sol.cpp as the judge's solution
prob.generateAnswers('sol.cpp')
