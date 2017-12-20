ECHO OFF
ECHO script

cd ..
python setup.py install
python setup.py build

cd gui

sleep 1

python paint.py


ECHO \nSee you later\n

ECHO Authors: \nInes Caldas \nJoel Carneiro\n

