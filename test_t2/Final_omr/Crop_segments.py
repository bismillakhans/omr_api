import cv2
import image_reg
import os

def crop(In_path,Out_path,Score_path):
    
    valid_images = [".jpg",".gif",".png",".tga"]

    for s in os.listdir(In_path):
        ext = os.path.splitext(s)[1]
        if ext.lower() not in valid_images:
            continue
        input_img=cv2.imread(os.path.join(In_path,s))
        

    Img_sizes=[]
    count = 0
    
    for f in os.listdir(Score_path):
        count+=1
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        imgs=cv2.imread(os.path.join(Score_path,f))
        Img_sizes.append([imgs.shape[0]*imgs.shape[1],f])
        
    
    #    cv2.imshow("Foreground", imgs )
    #    cv2.waitKey(0)
    
    Img_sizes.sort(reverse = True)
    
    for images in Img_sizes:
        img=  cv2.imread(Score_path+str(images[1]))
        detect=image_reg.alignImages(input_img,img)
        cv2.imwrite(Out_path+images[1],detect)
        Invert_detect=image_reg.alignImages(img,input_img)
        ret,thresh1 = cv2.threshold(Invert_detect,0,255,cv2.THRESH_BINARY_INV)
        thresh1 = cv2.cvtColor(thresh1, cv2.COLOR_BGR2GRAY)
        
        result = cv2.bitwise_and(input_img, input_img,mask=thresh1)
        input_img = result
    #    
#        cv2.imshow("Foreground", cv2.resize(input_img,(500,500)))
#        cv2.waitKey(0)
    
