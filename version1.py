

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

'''
作者：爱技术爱生活 
来源：CSDN 
原文：https://blog.csdn.net/tong5956/article/details/78392831 
版权声明：本文为博主原创文章，转载请附上博文链接！
'''