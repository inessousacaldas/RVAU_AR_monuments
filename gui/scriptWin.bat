@ECHO OFF
ECHO MonumentAR Application

cd ..
python setup.py install
python setup.py build

cd gui

timeout 1

python paint.py

ECHO.
ECHO See you later
ECHO.
ECHO Authors:
ECHO.
ECHO Ines Caldas 
ECHO.
ECHO Joel Carneiro
ECHO.

