

#file1 : 视频预览播放


import numpy as np
import time
import cv2

image = cv2.imread('./lalala.png')
cap = cv2.VideoCapture('./guge.wmv')
cv2.imshow('img',image)
cv2.waitKey(50)
time.sleep(5)
cv2.destroyWindow('img')
while (cap.isOpened()):
    ret, frame = cap.read()
    if frame is None:
        break
    else:
        cv2.imshow('video view', frame)
        if cv2.waitKey(40) & 0xFF == ord('Q'):
            break
cap.release()
cv2.destroyAllWindows()

