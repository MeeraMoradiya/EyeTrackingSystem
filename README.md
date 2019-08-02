# EyeTrackingSystem

**Virtual Keyboard operated by eye gaze**<br>
This is a school project implementd just for purpose of learning basics of Python for computer vision, Numpy and OpenCV libraries. The code may be duplicated as I have tried different approaches to implement same functionality

## Installation

git clone https://github.com/MeeraMoradiya/EyeTrackingSystem.git

## Requirements
Python 3.6 or 3.7<br>
dlib<br>
opencv<br>
numpy<br>
winsound<br>

## Description

Execute below command to run the application<br>
~~~
pip install -r requirements.txt
python final.py
~~~

final.py<br>
This file contains 3 frames for keyboard, notepad and camera the keyboard has selected key which can be moved using eye gaze. The selected letter will be written in the notepad if user blinks for 9 frames (user will be notified to open eyes using sound ) Using * key the written text can be converted to speech

<br>eye_detection.py</br>
This file is just to detect eye to learn basics of eye detection

<br>eye_motion_tracking.py</br>
To learn how to convert image into grey scale image using threshold by using opencv functions

## Licence

MIT

 

