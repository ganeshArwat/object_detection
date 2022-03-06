import cv2

thres = 0.45 # Threshold to detect object


img=cv2.imread('lena.png')

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
cap.set(10,70)

import os

# cwd = os.getcwd()  # Get the current working directory (cwd)
# files = os.listdir(cwd)  # Get all the files in that directory
# print("Files in %r: %s" % (cwd, files))

while True :

    success,img = cap.read()

    className=[]
    # classfile='Object_Detection_Files\coco.names'
    # classfile='coco.names'
    classfile='d1\Object_Detection_Files\coco.names'
    with open(classfile , 'rt') as f:
        className=f.read().rstrip('\n').split('\n')

    configPath = 'd1\Object_Detection_Files\ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = 'd1\Object_Detection_Files\Frozen_inference_graph.pb'
    # configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    # weightsPath = 'Frozen_inference_graph.pb'


    net = cv2.dnn_DetectionModel(weightsPath,configPath)
    net.setInputSize(320,320)
    net.setInputScale(1.0/ 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)


    classIds, confs, bbox = net.detect(img,confThreshold=thres)
    print(classIds,bbox)


    for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
        cv2.rectangle(img,box,color=(0,255,0),thickness=2)
        cv2.putText(img,className[classId-1].upper(),(box[0]+10,box[1]+30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)


    # print(className)

    cv2.imshow('output',img)
    # cv2.waitKey(1)
    k = cv2.waitKey(33)
    if k==27:    # Esc key to stop
        break