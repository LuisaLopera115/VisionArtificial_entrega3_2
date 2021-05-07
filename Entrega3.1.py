# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 18:05:43 2021

@author: ASUS
"""

import cv2
import time
import socket
import numpy as np
import math

UDP_IP = "127.0.0.1"
UDP_PORT = 5065

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rect = ['0'] # datos a enviar 

protoFile = "pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
weightsFile = "pose/mpi/pose_iter_160000.caffemodel"
nPoints = 15
#POSE_PAIRS = [[0,1], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [1,14], [14,8], [8,9], [9,10], [14,11], [11,12], [12,13] ]

inWidth = 128
inHeight = 128
threshold = 0.2

cap = cv2.VideoCapture(0)

hasFrame, frame = cap.read()
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

state = 0   

while (True):
    t = time.time()
    available, frame = cap.read()
    
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
        punto4x = 0 #mano
        punto4y = 0
        punto8x = 0 
        punto8y = 0
        punto3x = 0
        punto3y = 0
        punto2x = 0
        punto2y = 0
        punto0x = 0
        punto0y = 0
        punto1x = 0
        punto1y = 0
        punto14x = 0
        punto14y = 0
        punto7x = 0
        punto7y = 0
        punto11x = 0
        punto11y = 0
        punto6x = 0
        punto6y = 0
        punto5x = 0
        punto5y = 0
        derecho = False
        izquierdo = False
        for i in range(nPoints):            
            probMap = output[0, i, :, :] # confidence map of corresponding body's part.
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap) # Find global maxima of the probMap.                        
            x = (frameWidth * point[0]) / W # Scale the point to fit on the original image
            y = (frameHeight * point[1]) / H # Scale the point to fit on the original image
    
            if (prob > threshold) :
                cv2.circle(frame, (int(x), int(y)), 8, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
                points.append((int(x), int(y)))
               #cv2.putText(frame, "point"+str(i)+ " x: "+str(x)+" y: "+str(y), (int(x),int(y)), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255))
                if i == 4: # mano 
                    punto4x=x
                    punto4y=y
                if i == 1: # mano 
                    punto1x=x
                    punto1y=y
                if i == 14: # mano 
                    punto14x=x
                    punto14y=y
                if i == 8:
                    punto8x=x
                    punto8y=y
                if i == 3:
                    punto3x=x
                    punto3y=y
                if i == 2: #hombro izq
                    punto2x=x
                    punto2y=y
                if i == 5:# hombro dere
                    punto5x=x
                    punto5y=y
                if i == 0: # cabeza
                    punto0x=x
                    punto0y=y
                if i == 7: # mano
                    punto7x=x
                    punto7y=y
                if i == 11:
                    punto11x=x
                    punto11y=y
                if i == 6:
                    punto6x=x
                    punto6y=y
                
                    
                    
            else :
                points.append(None)
             
        # FORMA 1 
        """
        if punto2x > 0 and punto2y > 0 and punto5x > 0 and punto5y > 0 and punto1x > 0 and punto1y > 0 and punto14x > 0 and punto14y > 0:
            derecho=True
            
            cv2.line(frame, (int(punto2x),int(punto2y)),(int(punto5x),int(punto5y)),(255,0,0),2)
            cx=int((punto2x+punto5x)/2)
            cy=int((punto2y+punto5y)/2)
            cv2.line(frame, (int(cx),0),(int(cx),800),(255,0,0),2)
            
            unit_vector_1 = [punto2x,punto2y] / np.linalg.norm([punto2x,punto2y] )
            unit_vector_2 = [cx,800] / np.linalg.norm([cx,800])
            
            dot_product = np.dot(unit_vector_1, unit_vector_2)
            angle = np.arccos(dot_product)*180/3.14
            cv2.putText(frame,f'Angulo:' + str(angle) ,(20,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0))
            print(angle)
            
            
            mensaje = ",".join(rect)
            print((mensaje).encode())
            sock.sendto((mensaje).encode(), (UDP_IP,UDP_PORT))
          """
        # FORMA 2
        
        if punto7x > 0 and punto7y > 0 and punto4x > 0 and punto4y > 0:
            derecho=True
            
            cv2.line(frame, (int(punto4x),int(punto4y)),(int(punto7x),int(punto7y)),(255,0,0),2)
            distancia = math.sqrt((punto7x-punto4x)**2+(punto7y-punto4y)**2)
            
            if distancia >= 400 and distancia <= 500:
                diferncia = int(punto7y - punto4y)
                cv2.putText(frame,f'Diferencia:' + str(diferncia) ,(20,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0))
                cv2.putText(frame,f'Distancia:' + str(distancia) ,(100,80),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0))
                
                rect[0]= str(diferncia)
                mensaje = ",".join(rect)
                print((mensaje).encode())
                sock.sendto((mensaje).encode(), (UDP_IP,UDP_PORT))
        
        if punto7y<punto0y and punto7x < punto5x and punto7y<punto5y and punto6x>punto7x and punto6x>punto5x and punto7y < punto6y and punto6y < punto5y:
            izquierdo=True
        if izquierdo==True and derecho == True:
            cv2.putText(frame,f'pose: De egipcia (monos juntas por enciama de la cabeza ):3',(20,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0))
        cv2.imshow('Output-Skeleton', frame)
        
        
  
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()