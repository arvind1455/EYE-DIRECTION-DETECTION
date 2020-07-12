import cv2 
import numpy as np

def find_edge(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 80, 250, cv2.THRESH_BINARY_INV)
    blur = cv2.GaussianBlur(threshold,(7,7),0)
    kernel = np.ones((3,3), np.uint8)
    erosion = cv2.erode(blur, kernel, iterations=5)
    return erosion

def find_contours(center1, roi ,edges):
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = lambda x:cv2.contourArea(x), reverse = True )
    for cnt in contours:
        (x,y,w,h) = cv2.boundingRect(cnt)
        (x,y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)
        #cv2.circle(roi, center, radius, (0,0,255), 2)
        break
    #cv2.line(roi, (int(x), int(y)), (int(x), 70), (255,0, 0), 2)                               ## EYE CENTER LINE
    #cv2.circle(roi, center, 4, (255, 0, 255), 2)                                               ## EYE CENTER CIRCLE
    #cv2.line(frame, (center1-300,0), (center1-300, 1080), (0,255,0), 2)                        ## VIDEO CENTER LINE
    return frame, int(x), center

cap = cv2.VideoCapture("eyes.mp4")
out = cv2.VideoWriter('EYES DIRECTION.mp4', -1, 30, (1920, 1080))

while True:
    _, frame = cap.read()
    rows, cols, _ = frame.shape
    center1 = int(cols / 2)
    value = center1 - 300
    roi = frame[620:771, 380:858]
    edges = find_edge(roi)
    contours, x, center = find_contours(center1, roi, edges)

    #EYES DIRECTION CALCULATION    
    degrees = (x - (value/2)) * 0.061                                                           ## ALIGN EYES LINE WITH TARGET LINE
    if degrees > -3:
        cv2.putText(frame, "LOOKING LEFT", (1400,100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
    elif degrees > -6 and degrees < -2:
        cv2.putText(frame, "I AM LOOKING AT YOU ", (1200,100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
    elif degrees < -3:
        cv2.putText(frame, "LOOKING RIGHT", (1400,100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
    
    #SHOW AND SAVE THE OUTPUT
    out.write(frame)
    cv2.imshow("frame", frame)
    cv2.waitKey(1)