# MonumentAR

----------------------

# Authors

Inês Caldas

Joel Carneiro


----------------------

# Install

Before running the application it's necessary to install the dependencies. The versions in which the application was developed are below.

```
python --> 3.6.3
pillow --> 4.3.0
tk --> 8.6.7
matplotlib --> 2.1.1
numpy  --> 1.13.3
opencv --> opencv_python - 3.3.1
ghostscript --> Ghostscript 9.22 for Windows --> (https://www.ghostscript.com/download/gsdnld.html)

```


After the python environment has been created with the remaining dependencies of the application, the user must access the *scriptWin.bat* or *scriptUnix.sh* file, depending on his operating system, which is in the *Ar_monuments/gui* folder.


----------------------

# Introduction

Augmented Reality can be defined as an augmented view of the physical world through virtually generated elements. MonumentAR is an augmented reality application that "augments" facade images of buildings with visual elements. The recognition of facades is made using natural marks, not requiring fiducial marks.

The MonumentAR application integrates two subprograms, one of preparation and one of augmenting, which is abstracted in order to have a better interaction with the user. Thus, the user does not have to navigate through windows to complete their work.

The preparation subprogram allows the user to choose the regions of the images he wants to use to calculate the key points, to draw the "augmented" elements over the database images so that they appear overlaid on the test images in the "augmented" subprogram. The "augmented" subprogram has the function of comparing the images of the database and the image chosen as a test, calculating the homography matrix and presenting the results obtained.

The MonumentAR application was developed using the Python programming language, the OpenCV library for "augmented" section and the tkinter library for the graphical interface.

The program proved to be capable of solving the test problems efficiently, however, its speed depends proportionally on the algorithms chosen by the user and the size of the database. 

A more detailed description of the application will be presented in the next sections of the report, followed by the results obtained, their analysis and the conclusions drawn.


----------------------

# Application Description

MonumentAR was developed using the Python programming language and the OpenCV library for the "augmented" section and the tkinter library for the graphical interface.

After the user installs all the application dependencies and opens the application execution script, a window is displayed where the 
user can perform all the necessary tasks. The user must choose the images that he wants to use as a database. After this step, the user can upload one or more images to the database and paint on them the "marks" that he wants to present in the future images to be recognized. Various image editing tools are provided so that the user is free to build marks. After creating them, the user must save the marks.

He should also press the Key Points option to choose which region of the image to use for calculating the points of interest in the
image and remove the key points that he finds unnecessary. If he does not do this all image is considered for the calculation of the key points. The user can perform the same process for the remaining images that you want to put as a database. You can also access the database and delete or change the marks already made on one of the images. 

If the database is not empty, the user can test different facade images of buildings to see the augmented section on them according to the contents of the database. For this, there are two available algorithms, Scale-Invariant Feature Transform (SIFT) and Speeded-Up Robust Features (SURF). Also, the user can change the value of the the RANSAC threshold. The user can also choose the debug mode where all intermediate steps are displayed in the console and in the graphics.

As for the use of the * OpenCV * library, the following algorithms were used for the computation of * key points *, * descriptors * and matches:
```
  SIFT  - Scale-Invariant Feature Transform
  SURF - Speeded-Up Robust Features
  RANSAC [3] - Random sample consensus
  FLANN [4] - Fast Library for Approximate Nearest Neighbors 
```

----------------------

# Results

Different images were used, both in the database and in the test images, to test the developed application, to verify the execution time, if the homography matrix is ​​calculated correctly, and what type of influences can change the result of each algorithm. The tests were done using the SIFT and SURF algorithms with different values ​​assigned to the limit of the RANSAC algorithm.

It has been found that the SIFT algorithm is the most powerful. It always showed a good solution even when comparing images with different illuminations and different poses. 

As for the SURF algorithm, it was verified that, although it is faster in execution time than SIFT, the calculation of the homography, when it comes to images with different illuminations and not exactly frontal poses, it gives results that can be classified as bad. It is noteworthy that the homography that produced the best results considering the key points and descriptors of the SURF algorithm was when the image of the database and the image of the test were the same. Therefore, it can be concluded that with the SURF algorithm it's possible to calculate correct homographies, using SURF's key points and descriptors to calculate the matches, however, the results are susceptible to large variations depending on the lighting conditions and the pose of the images.

The FlannBasedMatcher method of the FLANN library was used to calculate the matches. This method is fairly efficient but matches are generated with only the approximate nearest neighbor, so they may not be the best. To overcome this constraint, the RANSAC algorithm was applied to the generated matches. It proved to be a good helper in calculating homographies, filtering out good matches from the wrong ones and eliminating the latter ones. 
The lower the value of the RANSAC limit, more erroneous matches are eliminated, resulting in a set of matches as correct as possible to calculate homography since this value represents the maximum allowable variation limit.
 


----------------------

# Referências

```
[1] - OpenCV: Introduction to SIFT (Scale-Invariant Feature Transform). (n.d.). Retrieved December 19, 2017, from https://docs.opencv.org/3.1.0/da/df5/tutorial_py_sift_intro.html

[2] - Introduction to SURF (Speeded-Up Robust Features) — OpenCV 3.0.0-dev documentation. (n.d.). Retrieved December 19, 2017, from https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_surf_intro/py_surf_intro.html

[3] - Feature Matching + Homography to find Objects — OpenCV 3.0.0-dev documentation. (n.d.). Retrieved December 19, 2017, from https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html

[4] - Feature Matching — OpenCV 3.0.0-dev documentation. (n.d.). Retrieved December 19, 2017, from https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_matcher/py_matcher.html
```

