#!/bin/bash

# $1: "run" or "test"
# $2: source filename

if [[ ( ! $1 == "run" ) && ( ! $1 == "test" ) ]]; then
  echo "1st arg must be 'run' or 'test'"
  exit
fi

if [[ $2 == "" ]]; then
  echo "2st arg must be source filename"
  exit
fi

os=`uname | tr '[:upper:]' '[:lower:]'` 
case $os in
  'windowsnt') os='win';;
  'darwin') os='mac';;
  *) os='';;
esac

name="${2%.*}"
runcmd=""

if [[ $2 == *.cpp ]]; then
  if [[ $os == 'win' ]]; then
    g++ -Wl,--stack,100000000 $2 -o $name -O2 -Wall -Wextra -std=gnu++0x || exit
  elif [[ $os == 'mac' ]]; then
    g++ -Wl,-stack_size,0x10000000 $2 -o $name -O2 -Wall -Wextra -std=gnu++0x || exit
  else
    g++ -fstack-limit-symbol=__stack_limit -Wl,--defsym,__stack_limit=0x10000000 -fstack-check $2 -o $name -O2 -Wall -Wextra -std=gnu++0x || exit
  fi
  runcmd="./$name"
elif [[ $2 == *java ]]; then
  # java class name must be the same as the file name
  javac $2
  runcmd="java $name"
elif [[ $2 == *py ]]; then
  runcmd="python $2"
else
  echo "unknown source type: $2"
  exit
fi

if [ ! -d "input" ]; then
  echo "No input folder found"
  exit 
elif [ ! "$(ls -A "input")" ]; then
  echo "Empty input folder"
  exit
fi
if [ ! -d "output" ]; then
  mkdir output
fi
if [[ ( ! -d "answer" ) && "$1" == "test" ]]; then
  mkdir answer
fi

for i in input/*; do
	echo -n -e "$i:\t"
	if [[ "$1" == "test" ]]; then
	  # test the src against all cases
  	$runcmd < $i > ${i//input/answer}
  	outfile=${i//input/output}
  	ansfile=${i//input/answer}
  	diffcmd="diff -q --strip-trailing-cr $outfile $ansfile"
  	comp=`eval $diffcmd`
  	if [[ "$comp" == "" ]]; then
  		echo "OK"
  	else
  		diff -y --strip-trailing-cr $outfile $ansfile
  		echo "INCORRECT"
  	fi
	else
	  # generate AC outputs for all cases
	  ansfile=${i//input/output}
	  ansfile=${ansfile//.in/.ans}
	  $runcmd < $i > $ansfile
	  echo "DONE"
	fi
done
