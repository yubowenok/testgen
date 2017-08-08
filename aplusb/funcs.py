import random

random.seed('aplusb')

def xMinusOne(args):
  x = args['x']
  return str(x) + ' -1\n'
  
def twoRandomIntegers(args):
  l, r = int(args['l']), int(args['r'])
  a, b = random.randint(l,r), random.randint(l,r)
  return str(a) + ' ' + str(b) + '\n'
