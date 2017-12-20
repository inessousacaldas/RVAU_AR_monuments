#!/bin/sh
echo -e "\nMonumentAR Application\n"

cd ..
python setup.py install
python setup.py build

cd gui

sleep 1

python paint.py

echo -e "\nSee you later\n"

echo -e "\nAuthors: \n\nInes Caldas\n \nJoel Carneiro\n"


