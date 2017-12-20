@ECHO OFF
ECHO database


cd ../database/vision/surf/descriptors
del *
cd ../keypoints
del *
cd ../images
del *

cd ../../sift/descriptors
del *
cd ../keypoints
del *
cd ../images
del *

cd ../../../images
del *

cd ../layers
del *

cd ../../gui

ECHO.
ECHO Database cleaned
ECHO.

