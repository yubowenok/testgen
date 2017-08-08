## Test generator for algorithm problems



### Test Generator and Runner

Here we show how to create test cases for a simple problem "A + B" that asks for the sum of two integers:

* Make a directory for the problem, say _aplusb_
* Download (clone) the testgen package. Make sure it is in sys.path.
We will be under _aplusb/_ in all the following steps.
* Create a folder for manual test cases, say _input\_manual_.
Add manual test case files to _input\_manual_.
Each file may contain arbitrary number of test cases, separated by a line with 20 equal signs, e.g.:
```
3 5
==================== case 3+5 (you can put any comments here)
4 7
==================== name:Sample-2 (you may specifically name the test file)
1 -1
```
* Write the test generator python scripts. 
The scripts shall have an entry file _gen.py_, which may follow the templates:
```python
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
```
* _funcs.py_ shall define several ways to generate tests programmatically, like:
```python
import random

random.seed('aplusb')

def xMinusOne(args):
  x = args['x']
  return str(x) + " -1\n"
  
def twoRandomIntegers(args):
  l, r = int(args['l']), int(args['r'])
  a, b = random.randint(l,r), random.randint(l,r)
  return str(a) + " " + str(b) + "\n"
```

* Write a generator rule file _aplusb.rules_. Rules file has simple syntax as follows:
```
group = MinusOne
  func = xMinusOne
  num = 2
  param
    x = 3
    x = 5
end

group = TwoRandom
  func = twoRandomIntegers
  num = 5
  param
    l = 1, r = 5
    l = 10, r = 20
    ...
end
```
Each group has a group name ("MinusOne" and "TwoRandom").
It tells the generator to call the method _func_ for this group of cases.
_func_ shall be called _num_ times, with the parameters specified by _param_.
Each _param_ line defines one set of parameter assignments separated by commas.
Three dots "..." may be used to repeat the last set of parameter assignments for the remaining test cases in this group.
In the above example, the last 4 cases for group "TwoRandom" all use parameters "l = 10, r = 20".

Note that rule files are space insensitive.
All spaces are ignored when a rule file gets parsed.

* Run the test generator
```
python gen.py
```
This shall create a folder named _input_ and put all cases there, one case per file.
The files are named _000.in_, _001.in_, and so on.
If there is a name set for a test case, it will be appended to the file name, e.g. _001-sample-1.in_.
Group names are automatically appended with its own counter, e.g. _008-MinusOne-1.in_.

* Write a solver for the problem, say _sol.cpp_
* Use _test\_runner.sh_ to generate the correct outputs for all the test cases, or test a solution
```
./test_runner.sh {run|test} sol.cpp
```
Source code will be compiled based on suffix file types. \*.cpp, \*.java and \*.py files are supported.
The correct outputs will be at _output/\*_.
For testing user's answers (to be compared against _output/\*_) will be at _answer/\*_.

To generate cases in a specific order, possibly with alternating manual and program generated cases, can be achieved by
modifying _gen.py_. This is particularly useful when the problem has multiple groups of inputs (subtasks), so
that the tests need to be combined with specific ordering.
```python
# small cases
prob.manualCases('input_manual_small')
prob.programCases('aplusb_small.rules', funcs)
# large cases
prob.manualCases('input_manual_large')
prob.programCases('aplusb_large.rules', funcs)
```


### Test Packer

You can use test packer to combine the test cases in the input folder into files with multiple test cases.
Each new case file will include multiple cases, prepending the number of cases at its beginning.
You need to write a group specification file (_aplusb.groups_) with the following format
```
n1 # number of cases in the 1st file
n2 # number of cases in the 2nd file
n3 # name:program number of cases in the 3rd file
...
```
Then in _gen.py_, add a call to test packer.
```Python
prob.packCases('aplusb.groups')
```
The first n1 cases (numbered by _001.in_, _002.in_ ...) will be written to the 1st input file (001.in),
the next n2 cases will be written to the 2nd input file (_002.in_), and so on.
If you name group in the groups file, the group name will also be added to the file name (such as _003-program.in_ in the example groups file).

Please make sure that the input folder contains sufficient number of cases.
If there are unused cases in the input folder, they will be deleted.

Test packer will give incorrect order if the number of cases exceed 999, as it sorts the input filenames lexicographically,
e.g. _1000.in_ appears before _999.in_.
It is not recommended to create more than 1000 cases.
If you have a problem that has a large number of cases, consider them to be multiple queries in one single case.



### Getting Started

The _create_problem.sh_ script may help you get started quickly. Use
```bash
./create_problem.sh {problem_id}
```
to initialize a problem with given id using the default template.
The files mentioned above will be initialized for you and you can just fill in their content.
