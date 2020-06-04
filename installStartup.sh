#!/bin/bash

if [[ $1 == "-h" ]] || [[ $1 == "--help" ]]; then
  echo -e "Installation script for the extensible sensor network to start on bootup\nMust be run as root\nRequires an absolute path to the python environment and a flag for the module type passed in (in that order)\n"
  echo -e "Acceptable modules are -c, -r, -m, -f"
  echo -e "These represent the camera module, radio network module, motor module, and fan module respectively"
  exit 0
fi

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

if [ "$#" -ne 2 ]; then
  echo "Unexpected number of parameters"
  exit 1
fi

if [[ $1 != /* ]]; then
  echo "Absolute path to project python enviironment needed"
  exit 1
fi

if expr match "$2" "-[crmf]"; then
  parameter="$2"
  echo $parameter
else
  echo "Proper flag not found"
  exit 2
fi

command="python /home/pi/CS179J-Team01/Source/main.py $parameter &"
echo $command

if [ ! -z $(grep "$command" "/etc/rc.local") ]; then
  echo "This network system already installed"
  exit 3
fi

projectpyenv="source"
projectpyenv="$projectpyenv $1"

printf '$-1i\n'${projectpyenv}'\n.\nw\n' | ed -s /etc/rc.local
printf '$-1i\n'${command}'\n.\nw\n' | ed -s "test.txt"

cat /etc/rc.local
echo "Installation successful"

exit 0
