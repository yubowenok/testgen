### Test generator for algorithm problems

Here we show how to create test cases for a simple problem "A + B" that asks for the sum of two integers:

* Make a directory for the problem, say _aplusb_
* Copy _test\_runner_ and _gen.py_ to _aplusb/_, then _cd_ to the directory.
We will be under _aplusb/_ in all the following steps.
* Create a folder for manual test cases, say _input\_manual_.
Add manual test case files to _input\_manual_.
Each file may contain arbitrary number of test cases, separated by a line with 20 equal signs, e.g.:
```
3 5
==================== case 3+5
4 7
==================== may put comments after the equal signs
1 -1
```
* Write the test generator python scripts. 
The scripts shall have an entry file _aplusb\_gen.py_,
which imports the common python package _gen.py_.
Follow the templates:
```python
import gen, aplusb_input

gen.init()

gen.manualCases("input_manual") # copy from the manual cases in input_manual
rules = gen.parseRule("aplusb.genrule") # parse the test generator rules defined in aplusb.genrule
gen.programCases(rules, aplusb_input) # generate tests via program, using the rules defined in aplub.gen
```
* _aplusb\_input.py_ shall define several ways to generate tests programmatically, like:
```python
import random

def xMinusOne(args):
  x = args['x']
  return str(x) + " -1\n"
  
def twoRandomIntegers(args):
  l, r = int(args['l']), int(args['r'])
  a, b = random.randint(l,r), random.randint(l,r)
  return str(a) + " " + str(b) + "\n"
```

* Write a generator rule file _aplusb.genrule_. Genrule file has simple syntax as follows:
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

* Run the test generator
```
python aplusb_gen.py
```
This shall create a folder named _input_ and put all cases there, one case per file.
The files are named _input00.txt_, _input01.txt_, and so on.

* Write a solver for the problem, say _sol.cpp_
* Use _test\_runner_ to generate the correct outputs for all the test cases, or test a solution
```
./test_runner {run|test} sol.cpp
```
Source code will be compiled based on suffix file types. \*.cpp, \*.java and \*.py files are supported.
The correct outputs will be at _output/\*_.
For testing user's answers (to be compared against _output/\*_) will be at _answer/\*_.