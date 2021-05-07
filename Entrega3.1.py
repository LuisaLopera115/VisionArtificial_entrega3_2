import cv2
import time
import socket
import numpy as np
import math

def distance(x, y):
    d = np.sqrt(np.power(y[0] - x[0], 2) + np.power(y[1] - x[1], 2))
    return d

def M(p1,p2):
    m = 0
    if (p1 is not None and p2 is not None):
        x = p2[0] - p1[0]
        y = p2[1] - p1[1]
        if x != 0:
            m = y/x
        else:
            m = -999
    return m

def ready(lst, total, rng, pos):
    p = True
    if len(lst) < total:
        p = False
    else:
        for i in range(rng + 1):
            if points[i] is None:
                p = False
                
        if pos is not None:        
            if points[pos] is None:
                p = False
        
    return p

UDP_IP = "127.0.0.1"
UDP_PORT = 5065

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rect = ['0'] # datos a enviar 

protoFile = "pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
weightsFile = "pose/mpi/pose_iter_160000.caffemodel"
nPoints = 8
inWidth = 168
inHeight = 168
threshold = 0.2

cap = cv2.VideoCapture(0)

hasFrame, frame = cap.read()
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

state = 0   

while (True):
    t = time.time()
    available, frame = cap.read()
    frame = cv2.flip(frame,1)
    
    if(state == 0):
        if(available): state = 1
    
    if(state == 1):
        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]
        state = 2
    
    if(state == 2):        
        inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False)
        net.setInput(inpBlob)
        output = net.forward()   
        H = output.shape[2]
        W = output.shape[3]                
        
        
        points = [] # Empty list to store the detected keypoints    
        for i in range(nPoints):            
            probMap = output[0, i, :, :] # confidence map of corresponding body's part.
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap) # Find global maxima of the probMap.                        
            x = (frameWidth * point[0]) / W # Scale the point to fit on the original image
            y = (frameHeight * point[1]) / H # Scale the point to fit on the original image
    
            if (prob > threshold) :
                cv2.circle(frame, (int(x), int(y)), 8, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)                  
                cv2.putText(frame, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, lineType=cv2.LINE_AA)                
                points.append((int(x), int(y)))                
                
            else :
                points.append(None)
    
    if ready(points,nPoints,7,None):
        print("Estan")
        if (math.fabs(M(points[2],points[3])-M(points[3],points[4])) < 0.65) and (math.fabs(M(points[5],points[6])-M(points[6],points[7])) < 0.65):            
            print("Por ahiiii")
            distancia = distance(points[4],points[7])
            diferncia = points[7][1] - points[4][1]
            
            if (math.fabs(M(points[4],points[2])-M(points[5],points[7])) < 0.5):
                cv2.line(frame, (int(points[4][0]),int(points[4][1])),(int(points[7][0]),int(points[7][1])),(255,0,0),2)
                cv2.putText(frame,f'Diferencia:' + str(diferncia) ,(20,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0))
                cv2.putText(frame,f'Distancia:' + str(distancia) ,(100,80),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0))
                
                rect[0]= str(diferncia)
                mensaje = ",".join(rect)
                print((mensaje).encode())
                sock.sendto((mensaje).encode(), (UDP_IP,UDP_PORT))
        else:
            rect[0]= str(0)
            mensaje = ",".join(rect)
            print((mensaje).encode())
            sock.sendto((mensaje).encode(), (UDP_IP,UDP_PORT))            
            
    cv2.imshow('Output-Skeleton', frame)              
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break                            

cap.release()
cv2.destroyAllWindows()