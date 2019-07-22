import cv2
import numpy as np
import dlib
from gaze_tracking import GazeTracking
import pyautogui as pag
from math import hypot
from numpy import array
import subprocess

cap = cv2.VideoCapture(0)
gaze = GazeTracking()
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
first_frame=None
#subprocess.Popen('C:\\Windows\\System32\\calc.exe')

# Keyboard settings
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
        return 'DOWN'
    elif ny < y - multiple * h:
        return 'UP'

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

def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

font = cv2.FONT_HERSHEY_PLAIN

def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    #hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
    #ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    ratio = hor_line_lenght / ver_line_lenght
    return ratio

def get_gaze_ratio(eye_points, facial_landmarks):
    left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                                (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                                (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                                (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                                (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                                (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)
    # cv2.polylines(frame, [left_eye_region], True, (0, 0, 255), 2)

    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [left_eye_region], True, 255, 2)
    cv2.fillPoly(mask, [left_eye_region], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)

    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])

    gray_eye = eye[min_y: max_y, min_x: max_x]
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    height, width = threshold_eye.shape
    left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
    left_side_white = cv2.countNonZero(left_side_threshold)

    right_side_threshold = threshold_eye[0: height, int(width / 2): width]
    right_side_white = cv2.countNonZero(right_side_threshold)

    if left_side_white == 0:
        gaze_ratio = 1
    elif right_side_white == 0:
        gaze_ratio = 5
    else:
        gaze_ratio = left_side_white / right_side_white
    return gaze_ratio

# Counters
frames = 0
letter_index = 0

while True:
    _, frame = cap.read()
    #frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
    
   
    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)
   
    keyboard[:] = (0, 0, 0)
    frames += 1
    new_frame = np.zeros((500, 500, 3), np.uint8)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    if first_frame is None:
        first_frame=frame
        frame_eye = array(gaze.frame_left_coords(first_frame))
        continue 

    faces = detector(gray)
    for face in faces:
        #x, y = face.left(), face.top()
        #x1, y1 = face.right(), face.bottom()
        #cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)

        landmarks = predictor(gray, face)

        # Detect blinking
        left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

        if blinking_ratio > 5.7:
            cv2.putText(frame, "BLINKING", (50, 150), font, 7, (255, 0, 0))


        # Gaze detection
        gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
        gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
        gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2

       
        drag=12
        
        
            
        left_pupil = array(gaze.pupil_left_coords())
        right_pupil = array(gaze.pupil_right_coords())
        w, h = 8, 8
        dir1=""
        mid_point=array([900,900])
        if left_pupil.size > 1 and right_pupil.size > 1:
            midpointx=(left_pupil[0]+right_pupil[0])/2
            midpointy=(left_pupil[1]+right_pupil[1])/2
        
            mid_point=array([midpointx,midpointy])
        
        if mid_point.size > 1 :
            dir1 = direction(mid_point, frame_eye, w, h)
            
            
            
        if gaze_ratio <= 1:
            cv2.putText(frame, "RIGHT", (50, 100), font, 2, (0, 0, 255), 3)
            pag.moveRel(drag, 0)
            new_frame[:] = (0, 0, 255)
        elif gaze_ratio > 1.7:
            new_frame[:] = (255, 0, 0)
            pag.moveRel(-drag, 0)
            cv2.putText(frame, "LEFT", (50, 100), font, 2, (0, 0, 255), 3)
        if dir1 == 'UP' :
            pag.moveRel(0, -drag)
            cv2.putText(frame, "UP", (150, 100), font, 2, (0, 0, 255), 3)
        elif dir1 == 'DOWN' :
            pag.moveRel(0, drag)
            cv2.putText(frame, "DOWN", (150, 100), font, 2, (0, 0, 255), 3)
        
       
        
         
     
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "direction: " + str(dir1), (90, 255), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        
        #if gaze.is_up():
        #    cv2.putText(frame, "UP", (500, 100), font, 2, (0, 0, 255), 3)
        #    pag.moveRel(0, drag)
        #elif gaze.is_down():
        #    cv2.putText(frame, "Down", (500, 100), font, 2, (0, 0, 255), 3)
        #    pag.moveRel(0, -drag)


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



    cv2.imshow("Frame", frame)
   
    

   # cv2.imshow("New frame", new_frame)
   # cv2.imshow("Virtual keyboard", keyboard)
   # cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

    

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
