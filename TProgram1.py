from multiprocessing import Process,Queue
import os
from keras.models import load_model
import numpy as np
import chineseText
import datetime
import cv2
import dlib

#********************************************************************************#
emotion_classifier = load_model('./simple_CNN.985-0.66.hdf5')
detector = dlib.get_frontal_face_detector()  # 使用默认的人类识别器模型
emotion_labels = {
        0: '生气',
        1: '厌恶',
        2: '恐惧',
        3: '开心',
        4: '难过',
        5: '惊喜',
        6: '平静'
    }

def play3(value):
    i=1
    while 1:
        if value.empty():
            '''
            demo1 = cv2.imread('./default/default %d.jpg' % i)
            # ret,img = demo1.read()
            cv2.imshow('demo', cv2.resize(demo1, (960, 540)))
            cv2.waitKey(20)
            i += 1
            if i == 20:
                i = 1
            '''
            print('**')
        else:
            if value.get()==1:
                demo1 = cv2.imread('./default/default%d.jpg' % i)
                # ret,img = demo1.read()
                cv2.imshow('demo', cv2.resize(demo1, (960, 540)))
                cv2.waitKey(2)
                i += 1
                if i == 20:
                    i = 1
            else:
                demo1 = cv2.imread('./view/default %d.jpg' % i)
                # ret,img = demo1.read()
                # ret, frame = cap.read()
                cv2.imshow('demo', cv2.resize(demo1, (960, 540)))
                cv2.waitKey(2)
                i += 1
                if i == 130:
                    i = 1

def detect(img,value):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dets = detector(gray, 1)
    print('0000000000000000000000000')
    if len(dets)==1:
        for face in dets:
            left = face.left()
            top = face.top()
            right = face.right()
            bottom = face.bottom()
            cv2.rectangle(img, (left, top), (right, bottom), (255, 255, 255),2)  #######cv2.rectangle(image, 左上角坐标, 右下角坐标, color)
            gray_face = gray[top:bottom, left:right]
            gray_face = cv2.resize(gray_face, (48, 48))
            gray_face = gray_face / 255.0
            gray_face = np.expand_dims(gray_face, 0)
            gray_face = np.expand_dims(gray_face, -1)
            emotion_label_arg = np.argmax(emotion_classifier.predict(gray_face))
            emotion = emotion_labels[emotion_label_arg]
            print(emotion)
            if emotion=="开心":
                value.put(0)
                print('23333')
            #play2()
            #p3.start()
            else:
                value.put(1)
            img = chineseText.cv2ImgAddText(img, emotion, right * 0.75, top * 0.9, (255, 0, 0), 20)
        #return img
            cv2.imshow("view", cv2.resize(img, (1024, 600)))
            #cv2.imshow("view",img)
    else:
        value.put(1)
        cv2.imshow("view",cv2.resize(img, (1024, 600)))
        #cv2.imshow("view", img)

def Preview(value):
    startTime = datetime.datetime.now()
    while 1:
        cap = cv2.VideoCapture(0)
        #cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
        #cap.set(cv2.CAP_PROP_FRAME_HEIGHT,768)
        #i=0
        while cap.isOpened():
            ret, frame = cap.read()
            #i+=1
            detect(frame,value)
            #cv2.imshow('view',image)
            endTime = datetime.datetime.now()
            runTime = endTime - startTime
            print(runTime)
            '''
            if (runTime)>10:
                cap.release()
                cv2.destroyWindow('view')
                break
            '''
            cv2.waitKey(2)
        else:
            print('6666')
            break
    cap.release()
def draw_circle(event, x, y, flags, value):
    if event == cv2.EVENT_LBUTTONDOWN:
        Preview(value)
#******************************************************************************#
def PreviewProcess(value):
    background = cv2.imread('./background.png')
    #value.put(1)
    while (1):
        cv2.imshow('view', cv2.resize(background, (1024, 600)))
        cv2.waitKey(5)
        cv2.setMouseCallback('view', draw_circle,value)
#***********************************************************************************#


if __name__=='__main__':
    value=Queue()
    #value.put(2)
    print('Parent process %s.' % os.getpid())
    p1 = Process(target=PreviewProcess,args=(value,))
    p2 = Process(target=play3,args=(value,))
    print('Child process will start.')
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print('Child process end.')