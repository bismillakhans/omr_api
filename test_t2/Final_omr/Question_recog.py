import cv2
import numpy as np

def answer(x):
    
    if  0<x<90:
        ans ="a"
    if  90<x<180:
        ans ="b"
    if  180<x<270:
        ans ="c"
    if  270<x<360:
        ans ="d"
        
    return ans
    
def question():  
    orginal=cv2.imread("Aligned/Question.png",0)
    
    th, im_th = cv2.threshold(orginal,127,255,0)
    
    im_th=~im_th
    kernel = np.ones((4,4), np.uint8) 
    binary = cv2.erode(im_th, kernel, iterations=2) 
    
    h,w = binary.shape                   
    
    question = 0
    question_array = [""]*201
    for y in range(0, w,np.uint(np.floor(w/5))): 
        
        if (y +int(w/5-15) > w):
            break 
            
        if y== 0:
            column = binary[14:h-6, y+75: y +int(w/5-15)]
            visc= orginal[14:h-6, y: y +int(w/5-15)]
        
        else:
            column = binary[14:h-6, y+90: y +int(w/5-15)] 
#            visc= orginal[14:h-6, y+14: y +int(w/5-15)] 
                          
    #    cv2.imshow("Foreground", visc)
    #    cv2.waitKey(0)
    ##column = orginal[15:1696, 0:420] 
    
        for x in range(0, column.shape[0],np.uint(np.floor(h/40))):
                    
            if (x+40 > h):
                break  
            
            question+=1
            row = column[x:x+40,:] 
#            visr=visc[x:x+40,:]    
    #        cv2.imshow("Foreground", visr)
    #        cv2.waitKey(0)
    
            (_,cnts, _) = cv2.findContours(row, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
            
            
            if len(cnts) <= 0 :
                
             question_array[question] = "" 
               
    # if cv2.contourArea(cnts[0])>950 or cv2.contourArea(cnts[0]) <600:
    #                
            elif len(cnts) ==  1:                          
                
                M = cv2.moments(row)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                            
                question_array[question] = answer(cX)
    
            elif len(cnts) ==  2:
                
                M1 = cv2.moments(cnts[1])
                cX1 = int(M1["m10"] / M1["m00"])
                cY1 = int(M1["m01"] / M1["m00"])
            
                
                M2 = cv2.moments(cnts[0])
                cX2 = int(M2["m10"] / M2["m00"])
                cY2 = int(M2["m01"] / M2["m00"])
                
                question_array[question] = answer(cX1)+answer(cX2)
                
            elif len(cnts) ==  3:
                
                M1 = cv2.moments(cnts[2])
                cX1 = int(M1["m10"] / M1["m00"])
                cY1 = int(M1["m01"] / M1["m00"])
            
                
                M2 = cv2.moments(cnts[1])
                cX2 = int(M2["m10"] / M2["m00"])
                cY2 = int(M2["m01"] / M2["m00"])
                
                M3 = cv2.moments(cnts[0])
                cX3 = int(M3["m10"] / M3["m00"])
                cY3 = int(M3["m01"] / M3["m00"])
                
                question_array[question] = answer(cX1)+answer(cX2)+answer(cX3)
            else:
                question_array[question]="a,b,c,d"
#            print(question,question_array[question])
            
    return question_array            


            