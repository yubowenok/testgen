#!/bin/bash

# $1: problem id

if [[ $1 == "" ]]; then
  echo "Usage: ./init.sh {problem_id}"
  exit 1
fi

problem_id=$1

if [[ -d "$1" ]]; then
  echo "Problem with that id already exists. If you want to create a new problem with that id, remove the folder first."
  exit 1
fi

cp -R template $1

mv $1/template.groups $1/$1.groups
mv $1/template.rules $1/$1.rules

sed -i.bak s/template/$1/g $1/gen.py
rm $1/gen.py.bak
sed -i.bak s/template/$1/g $1/funcs.py
rm $1/funcs.py.bak
