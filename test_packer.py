#!/usr/bin/python
import os, sys

num_files = int(raw_input().rstrip("\r\n").split(" ")[0])

file_sizes = []

for i in range(num_files):
  tokens = raw_input().rstrip("\r\n").split(" ")
  file_sizes.append(int(tokens[0]))

file_counter = 0

def getNextTmpFilename():
  global file_counter
  res = ""
  if file_counter < 10:
    res = "input00" + str(file_counter) + ".tmp"
  elif file_counter < 100:
    res = "input0" + str(file_counter) + ".tmp"
  file_counter = file_counter + 1
  return res

for dirname, dirnames, filenames in os.walk("input"):
  global failed
  filenames = sorted(filenames)
  counter = 0
  for file_sizes_i in range(len(file_sizes)):
    new_filepath = os.path.join(dirname, getNextTmpFilename())
    out_file = open(new_filepath, 'w')
    contents = ""
    for i in range(counter, counter + file_sizes[file_sizes_i]):
      if i >= len(filenames):
        print >> sys.stderr, "Error: not enough input files"
        sys.exit(1)
        break
      filepath = os.path.join(dirname, filenames[i])
      file = open(filepath, 'r')
      lines = file.readlines()
      file.close()
      contents = contents + "".join(lines)
    contents = str(file_sizes[file_sizes_i]) + "\n" + contents
    out_file.write(contents)
    out_file.close()
    counter = counter + file_sizes[file_sizes_i]
  
  if counter < len(filenames):
    print >> sys.stderr, "Warning: not all input files were used"

for dirname, dirnames, filenames in os.walk("input"):
  for filename in filenames:
    if filename[-4:] == ".txt":
      filepath = os.path.join(dirname, filename)
      os.remove(filepath)
 
  for filename in filenames:
    if filename[-4:] == ".tmp":
      new_filename = filename[:-4] + ".txt"
      filepath = os.path.join(dirname, filename)
      new_filepath = os.path.join(dirname, new_filename)
      os.rename(filepath, new_filepath)
