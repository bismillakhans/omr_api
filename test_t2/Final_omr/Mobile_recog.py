import cv2
import numpy as np

def mobile():
    
    orginal=cv2.imread("Aligned/Mobile_number.png",0)
        
    h,w = orginal.shape
    crop= orginal[200:h-9,15:w-15]
    th, im_th = cv2.threshold(crop,127,255,0)
    im_th=~im_th
    kernel = np.ones((5,5), np.uint8) 
    binary = cv2.erode(im_th, kernel, iterations=2) 
    h1,w1 = crop.shape
    
    number=[]
    
    
    for y in range(0, w1,np.uint(np.floor(w1/10))):
        
        if (y +int(w1/10) > w1):
            break 
        column = binary[0:h1, y: y +int(w1/10)]
        visc=crop[0:h1, y: y +int(w1/10)]
        countn = 0 
        for x in range(0, h1,np.uint(np.floor(h1/10))):
           
            if (x+int(h1/10) > h1):
                   break
            row = column[x:x+int(h1/10),:] 
            visr=visc[x:x+int(h1/10),:] 
            countn+=1
            (_,cnts, _) = cv2.findContours(row, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)       
            if len(cnts) == 1: 
                number.append(str(countn))
    
    number=[0 if x == 10 else x for x in number]
    number=''.join(number)
    number=int(number)

    return number

        

   