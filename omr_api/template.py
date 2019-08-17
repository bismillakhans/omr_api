import numpy as np
import cv2
# import image_reg

def match(img,template):

    image = img #cv2.imread('temp/2.png')
    template = template
    # resize images
    image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)
    template = cv2.resize(template, (0,0), fx=0.5, fy=0.5)
    
    # Convert to grayscale
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
    #ret, imageGray = cv2.threshold(imageGray, 120, 255, cv2.THRESH_TOZERO) 
    #ret, templateGray = cv2.threshold(templateGray, 120, 255, cv2.THRESH_TOZERO) 
    
    
    # Find template
    result = cv2.matchTemplate(imageGray,templateGray, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    h,w = templateGray.shape
    bottom_right = (top_left[0] + w, top_left[1] + h)
    
    # Show result
    #cv2.imshow("Template", template)
    #z=image[top_left[1]-20:bottom_right[1]+20,top_left[0]-20:bottom_right[0]+20]
    
    temp_img=image.copy()
    segment=temp_img[top_left[1]:bottom_right[1],top_left[0]:bottom_right[0]]

    return segment
#cv2.rectangle(image,top_left, bottom_right,(0,0,255),4)
#cv2.imshow("Foreground", image)
#cv2.waitKey(0)