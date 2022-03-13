import cv2
import numpy as np
import os

cwd = os.getcwd()
print("Current working directory:", cwd)

thres = 0.45 # Threshold to detect object
nms_threshold=0.2 #0-1 0==lessbox 1==moreboxes

img=cv2.imread('lena.png')

cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
cap.set(10,70)

voice='espeak "detecting object"'
os.system(voice)
for k in range(2) :

    success,img = cap.read()

    className=[]
   # classfile='d1\Object_Detection_Files\coco.names'
    #classfile='coco.names'
    classfile='1 object detection/d1/Object_Detection_Files/coco.names'
    with open(classfile , 'rt') as f:
        className=f.read().rstrip('\n').split('\n')

    #configPath = 'd1\Object_Detection_Files\ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    #weightsPath = 'd1\Object_Detection_Files\Frozen_inference_graph.pb'

    #configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    #weightsPath = 'Frozen_inference_graph.pb'

    configPath = '1 object detection/d1/Object_Detection_Files/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = '1 object detection/d1/Object_Detection_Files/Frozen_inference_graph.pb'


    net = cv2.dnn_DetectionModel(weightsPath,configPath)
    net.setInputSize(320,320)
    net.setInputScale(1.0/ 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)


    classIds, confs, bbox = net.detect(img,confThreshold=thres)
    #print(classIds,bbox)
    bbox = list(bbox)
    confs = list(np.array(confs).reshape(1,-1)[0])
    confs = list(map(float,confs))
    #print(type(confs[0]))
    #print(confs)

    indices = cv2.dnn.NMSBoxes(bbox,confs,thres,nms_threshold)
    #print(indices)


    for i in indices:
        # i=i[0]
        #print(i)
        #print("bbox")
        #print(bbox.array[i])
        box=bbox[0]
        #print(box)
        x,y,w,h = box[0],box[1],box[2],box[3]
        cv2.rectangle(img, (x,y),(x+w,h+y), color=(0, 255, 0), thickness=2)
        #print(className)
        #print(classIds[0][0])
        cv2.putText(img,className[classIds[0][0]-1].upper(),(box[0]+10,box[1]+30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
        
        print(className[classIds[0][0]-1].upper())
        objectvoice='espeak "'+className[classIds[0][0]-1].upper()+'"'
        #print(objectvoice)
        os.system(objectvoice)



    # for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
    #     cv2.rectangle(img,box,color=(0,255,0),thickness=2)
    #     cv2.putText(img,className[classId-1].upper(),(box[0]+10,box[1]+30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
    #     cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)


    # print(className)

    #cv2.imshow('output',img)
    # key=cv2.waitKey(1)
    k = cv2.waitKey(33)
    if k==27:    # Esc key to stop
        break
    

    
