import gen, aplusb_input

gen.init()

gen.manualCases("input_manual") # copy from the manual cases in input_manual
rules = gen.parseRule("aplusb.genrule") # parse the test generator rules defined in aplusb.genrule
gen.programCases(rules, aplusb_input) # generate tests via program, using the rules defined in aplub.gen