#Importing the Dependencies :
import cv2
import os
import shutil
import time

class VideoCamera(object):
    def __init__(self,
                cam_index:int =0,
                roi_size:int=200):
        
        #Setting Some init values :
        self.video = cv2.VideoCapture(cam_index)
        self.window_size = roi_size //2
        self.prev_frame_time = 0
        self.new_frame_time = 0

    def __del__(self):
        # killing the Camera frame func:
        self.video.release()
    

    def get_frame(self,c,path):
        #reading image from the Camera :
        ret, img = self.video.read()
        
        #Extracting the image shape. (the shape is 480x640 at lot of cases):
        imgShape = img.shape

        #Extarcting the the image center cordinate to draw the lines and the roi rectangle depends on the roi size :
        centerCord = (imgShape[1]//2, imgShape[0]//2)

        #Cropping the image(the region of intrest):
        roi = img[centerCord[1]-self.window_size:centerCord[1]+self.window_size,
                centerCord[0]-self.window_size:centerCord[0]+self.window_size]

        #saving the ROI to the path:
        if c == 1 :
            if not(path==""):

                    #Writing the image :
                    cv2.imwrite(path+f"/{time.time()}.png",roi)
        
        #Drawing Some lines :
        cv2.line(img,
                (imgShape[1]//2,0),
                (centerCord[0],centerCord[1]-self.window_size),
                color=(0,0,250),
                thickness=2)

        cv2.line(img,
                (0,imgShape[0]//2),
                (centerCord[0]-self.window_size,centerCord[1]),
                color=(0,0,250),
                thickness=2)
        
        cv2.line(img,
                (imgShape[1],imgShape[0]//2),
                (centerCord[0]+self.window_size,centerCord[1]),
                color=(0,0,250),
                thickness=2)
        
        cv2.line(img,
                (imgShape[1]//2,imgShape[0]),
                (centerCord[0],centerCord[1]+self.window_size),
                color=(0,0,250),
                thickness=2)

        #Drawing the ROI on the img(Frame):
        cv2.rectangle(img=img,
                    pt1=(centerCord[0]-self.window_size,centerCord[1]-self.window_size),
                    pt2=(centerCord[0]+self.window_size,centerCord[1]+self.window_size),
                    color=(255,255,0),
                    thickness=1)

        #Calculating the FPS :
        self.new_frame_time = time.time()
        fps = 1/(self.new_frame_time-self.prev_frame_time)

        self.prev_frame_time = self.new_frame_time
        fps = int(fps)

        #Encode the image :
        ret, jpeg = cv2.imencode('.jpg', img)

        #Returning the image encoded and convert it into bytes with fps:
        return jpeg.tobytes(), fps