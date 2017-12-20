ECHO OFF
ECHO database

cd ../database/vision/surf/descriptors
rm *
cd ../keypoints
rm *
cd ../images
rm *

cd ../../sift/descriptors
rm *
cd ../keypoints
rm *
cd ../images
rm *

cd ../../../../gui

ECHO.
ECHO Database cleaned
ECHO.