import random

random.seed('template')

def rand(a,b):
  return random.randint(a,b)

# Create functions here to be called by programCases
def dummyRandom(args):
  max_random = int(args['max_random'])
  return str(rand(1, max_random)) + '\n'
