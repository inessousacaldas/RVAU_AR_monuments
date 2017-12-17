ECHO script

cd ..
python setup.py install
python setup.py build

cd vision

python ar_labeling.py

ECHO done

