"""
Demonstration of the GazeTracking library.
Check the README.md for complete documentation.
"""

import cv2
from gaze_tracking import GazeTracking
import pyautogui as pag
import numpy as np
from numpy import array

gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
first_frame=None


keyboard = np.zeros((600, 1000, 3), np.uint8)
keys_set_1 = {0: "Q", 1: "W", 2: "E", 3: "R", 4: "T",
              5: "A", 6: "S", 7: "D", 8: "F", 9: "G",
              10: "Z", 11: "X", 12: "C", 13: "V", 14: "B"}
              

def direction(nose_point, anchor_point, w, h, multiple=1):
    
    nx=nose_point[0]
    ny=nose_point[1]
    x=anchor_point[0]
    y=anchor_point[1]
    
    if ny > y + multiple * h:
        return 'down'
    elif ny < y - multiple * h:
        return 'up'

    return '-'              
              
def letter(letter_index, text, letter_light):
    # Keys
    if letter_index == 0:
        x = 0
        y = 0
    elif letter_index == 1:
        x = 200
        y = 0
    elif letter_index == 2:
        x = 400
        y = 0
    elif letter_index == 3:
        x = 600
        y = 0
    elif letter_index == 4:
        x = 800
        y = 0
    elif letter_index == 5:
        x = 0
        y = 200
    elif letter_index == 6:
        x = 200
        y = 200
    elif letter_index == 7:
        x = 400
        y = 200
    elif letter_index == 8:
        x = 600
        y = 200
    elif letter_index == 9:
        x = 800
        y = 200
    elif letter_index == 10:
        x = 0
        y = 400
    elif letter_index == 11:
        x = 200
        y = 400
    elif letter_index == 12:
        x = 400
        y = 400
    elif letter_index == 13:
        x = 600
        y = 400
    elif letter_index == 14:
        x = 800
        y = 400

    width = 200
    height = 200
    th = 3 # thickness
    #if letter_light is True:
    #    cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
    #else:
    cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (255, 0, 0), th)

    # Text settings
    font_letter = cv2.FONT_HERSHEY_PLAIN
    font_scale = 10
    font_th = 4
    text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x
    text_y = int((height + height_text) / 2) + y
    cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (255, 0, 0), font_th)

frames = 0
letter_index = 0

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    if first_frame is None:
        first_frame=frame
        frame_eye = array(gaze.frame_left_coords(first_frame))
        continue     

    frame = gaze.annotated_frame()
    
    keyboard[:] = (0, 0, 0)
    frames += 1
    
    text = ""
    drag = 12
    if gaze.is_blinking():
        text = "Blinking"
        #pag.click(button='left')
    elif gaze.is_right():
        text = "Looking right"  
      #  pag.moveRel(drag, 0)
    elif gaze.is_left():
        text = "Looking left"
       # pag.moveRel(-drag, 0)
    elif gaze.is_up():
        text = "Looking Up"
    elif gaze.is_down():
        text = "Looking Down"
    elif gaze.is_center():
        text = "Looking center"

    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    left_pupil = array(gaze.pupil_left_coords())
    right_pupil = array(gaze.pupil_right_coords())
    w, h = 8, 8
    dir1=""
    if left_pupil.size > 1 and right_pupil.size > 1:
        midpointx=(left_pupil[0]+right_pupil[0])/2
        midpointy=(left_pupil[1]+right_pupil[1])/2
    
        mid_point=array([midpointx,midpointy])
    
    if mid_point.size > 1 :
        dir1 = direction(mid_point, frame_eye, w, h)
    
    
    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    
   
    cv2.putText(frame, "direction: " + str(dir1), (90, 255), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    
   
   
     # Letters
    if frames == 10:
        letter_index += 1
        frames = 0
    if letter_index == 15:
        letter_index = 0


    for i in range(15):
        if i == letter_index:
            light = True
        else:
            light = False
        letter(i, keys_set_1[i], light)


   
    cv2.imshow("Demo", frame)
    #cv2.imshow("Virtual keyboard", keyboard)
   

    if cv2.waitKey(1) == 27:
        break
