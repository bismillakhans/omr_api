import cv2
import numpy as np

alpha =['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def name():    
    orginal=cv2.imread("Aligned/Name.png",0)
    
    h,w = orginal.shape
    crop= orginal[155:h-20,28:w-30]
    th, im_th = cv2.threshold(crop,127,255,0)
    im_th=~im_th
    kernel = np.ones((5,5), np.uint8) 
    binary = cv2.erode(im_th, kernel, iterations=2) 
    
    h1,w1 = crop.shape
    name=[]
    
    #cv2.imshow("Foreground", crop )
#    cv2.waitKey(0)

    for y in range(0, w1,np.uint(np.floor(w1/29))):
        
        if (y +int(w1/29) > w1):
            break 
        column = binary[10:h1, y: y +int(w1/29)]
        visc=crop[10:h1, y: y +int(w1/29)]
        countn = 0 
        
        for x in range(0, h1,np.uint(np.floor(h1/26))):
            
            if (x+int(h1/26) > h1):
                break
            row = column[x:x+int(h1/26),:] 
            visr=visc[x:x+int(h1/26),:] 
            countn+=1
    #        cv2.imshow("Foreground", visr )
    #        cv2.waitKey(1)

            (_,cnts, _) = cv2.findContours(row, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)       
            if len(cnts) == 1: 
                name.append(alpha[countn-1])
    
    name=''.join(name)
    return name
