# Created by TestGen
# https://github.com/yubowenok/testgen

import sys

# add testgen to system path, or include the path here
sys.path.append('../..')

from testgen import Problem
import funcs

# create a new problem instance with given id
prob = Problem('template')

# copy from the manual cases in input_manual
prob.manualCases('input_manual')

# parse the test generator rules defined in the file "template.rules",
# and generate tests via program using the rules
prob.programCases('template.rules', funcs)

# Group the cases into smaller number of files
# to create multpile subtasks or be compatible with non single-case judges.
# Use this only if you need case packing.
prob.packCases('template.groups')

# generate answers using sol.cpp as the judge's solution
prob.generateAnswers('sol.cpp')
