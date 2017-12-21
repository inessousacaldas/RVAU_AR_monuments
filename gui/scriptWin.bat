@echo OFF
echo MonumentAR Application

cd ..
python setup.py install
python setup.py build

cd gui

timeout 1

python paint.py

echo.
echo See you later
echo.
echo Authors:
echo.
echo Ines Caldas 
echo.
echo Joel Carneiro
echo.

