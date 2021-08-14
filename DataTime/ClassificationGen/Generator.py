import cv2 
import numpy as np 
import os
import sys
import shutil
from tqdm import tqdm
import matplotlib.pyplot as plt
import time 
import pickle
import json

class DataImageGenerator():
    def __init__(self, 
                path:str):
        #path of images :
        self.path = path

        #Lists Objects for generating and analyzing the Data:
        self.ClassData = [] 
        self.imagesPath = []
        self.classCounter = 0
        self.classNames = []
        self.imagesLabels =[]
        self.newPathsofSaving =[]
        
        #lists for the output Data:
        self.outputImages = []
        self.OutputLabelsNames = []
        self.dataTypeInformations = {"NoOfClasses": 0,
                                    "TotalImages" : 0,
                                    "TotalLabelsList": 0
                                    }
        self.LabelsExtracted = {"Labels":list,
                                "LabelsEncoded":list
                                    }
    def PathCorrector(self,
                    p:str):
                    
        #WindowsOS gives errors on paths, so we can fix it by  replacing "\" to "/":
        if sys.platform == "win32":
            p = p.replace("\ "[0],"/")
        return p

    def FirstImagePaths(self):

        #Verifying if classData attribute is empty cause errors problems
        self.ClassData = []
        
        #Extacting the first path to the classes directories:
        for i in os.listdir(self.path):
            dirPath = os.path.join(self.path,i)
            dirPath = self.PathCorrector(dirPath)
            self.ClassData.append(dirPath)
            self.classCounter = self.classCounter + 1
        
        #adding number of classes to dataTypeInformations dict:
        self.dataTypeInformations["NoOfClasses"] = self.classCounter
        
        #returning the first directory of the data:
        return self.ClassData

    def DataToArray(self):
        
        #generating the data paths via extarting the class names , images and labels values into lists:
        imagesPathsToData = self.FirstImagePaths()
        
        for i in range(self.classCounter):
            
            #browssing into each directory to extract images for each class:
            for j in os.listdir(imagesPathsToData[i]):
                
                #ignoring the Label directory to save only images:
                if not(j == "Label"):
                    
                    #appending images paths to imagesPath list:
                    p = os.path.join(imagesPathsToData[i], j)
                    p = self.PathCorrector(p)
                    self.imagesPath.append(p)

                    #appending class names paths to classNames list:
                    self.classNames.append(imagesPathsToData[i][imagesPathsToData[i].rindex("/")+1:])
                else:
                    
                    #appending and browsing the Label directory into imagesLabels list to extract the path of files:
                    lp = os.path.join(imagesPathsToData[i],"label".capitalize())
                    lp = self.PathCorrector(lp)
                    for k in os.listdir(lp):
                        l=os.path.join(imagesPathsToData[i],"Label",k)
                        l=self.PathCorrector(l)
                        self.imagesLabels.append(l)
        
        #returning 3 lists containing the paths of informations of each image:    
        return self.imagesPath , self.classNames , self.imagesLabels

    def DataVerification(self,
                    images_path:list,
                    class_names:list,
                    images_labels:list):
        
        #verifiying the correct loading of the images paths and inforamtions:
        verif  = True 
        
        #browsing into paths, names and data inforrmations:
        for i in range(0,len(images_path)):
            
            length = len(class_names[i])
            ClassNameIndexFromImagesPathList = images_path[i].rindex(class_names[i])
            ClassNameIndexFromImagesLabelsList = images_labels[i].rindex(class_names[i])
            image = images_path[i][ClassNameIndexFromImagesPathList+length+1:-4]
            label = images_path[i][ClassNameIndexFromImagesLabelsList+length+1:-4]
            
            if label == image and len(images_path) == len(images_labels) and len(images_labels)== len(class_names) :
                verif = True
            else:
                verif = False
                
            if verif == False :
                raise ValueError("Can't load the data Correctly, please check the right data path.")
        return verif

    def DataExtarction(self,
                    images_path:list,
                    class_names:list,
                    images_labels:list,
                    NewSize:tuple):
        
        #extarcting the objects from each image:
        #labels list for informations of the cropped image:
        labels =  []
        
        #browsing the hole lists returned by DataToArray Function:
        print("Generaring your custom Data ...")
        for img in tqdm(range(len(images_path))):
            
            #loading the image using opencv
            image = cv2.imread(images_path[img])
            
            #reading the label file:
            with open(images_labels[img],'r') as t :
                
                #converting data from file to list object:
                labels = t.read().rstrip("\n").split("\n")
                for j in range(len(labels)):
                    
                    labels[j] = labels[j].split(" ")
                    for e in range(len(labels[j])):
                        
                        #changing Value of className into None Object
                        if "A" <=labels[j][e].upper() <= "Z":
                            labels[j][e] = None 
                        else :
                            
                            #converting values from string to Float numbers then Integers:
                            try :
                                labels[j][e] = int(float(labels[j][e]))
                            
                            except Exception as e :
                                labels[j][e] = int(labels[j][e])
            
                    #start point : xmin , ymin (informations from data generated)
                    startPoint = (labels[j][1], labels[j][2])
                    
                    #end point : xmax , ymax (informations from data generated)
                    endPoint = (labels[j][3] , labels[j][4])
                    
                    #Cropping the new image:
                    newImage = image[startPoint[1]:endPoint[1],
                                    startPoint[0]:endPoint[0]]
                    
                    #Verifying the images cropped shape existance :
                    if 0 in newImage.shape:
                        continue
                    else:
                        
                        #resizing the images to the recommended size demanded by the model architecture:
                        newImage = cv2.resize(newImage, NewSize, cv2.INTER_AREA)

                        #appending the cropped images to outputImages list:
                        self.outputImages.append(newImage)
                    
                        #appending the cropped images class names to outputLabelsNames list:
                        self.OutputLabelsNames.append(class_names[img])

        #encrypting Labels (converting each class name into integers) (encoding the class names):
        count = 0
        initLabel = self.OutputLabelsNames[0]
        EncodedLabelsList = []
        for l in range(len(self.OutputLabelsNames)):
            if self.OutputLabelsNames[l] == initLabel:
                EncodedLabelsList.append(count)
            else:
                count = count + 1
                initLabel = self.OutputLabelsNames[l]
                EncodedLabelsList.append(count)

        self.LabelsExtracted["LabelsEncoded"] = EncodedLabelsList
        print("Generation Process completed succesfully.\n")

        #returning the results via outputImages and OutputLabelsNames lists:
        return self.outputImages, self.OutputLabelsNames
    
    def GenerateBalanceValue(self,
                            OutputImages,
                            OutputLabelsNames,
                            OutputLabelsEncoded,
                            display=False):

        #Defining new lists for extarct Data
        data = np.array(OutputLabelsEncoded)
        NewData , NewImages, NewLabels = [],[],[]
        numOfSamples = []
        NewNumOfSamples = []
        ReturnedImages = []
        ReturnedLabels = []
        ReturnedLabelsEncoded = []
        
        #Defining the DeadNumOfData to the balance process
        deadNumOfData = 500
        
        #Extract Each data with the same className :
        for x in range(0,max(data)+1):

            #Finding the indexs of each className on data list to split it into multidimensional list :
            arr = np.where(data==x)[0]
            numOfSamples.append(len(arr))
            i =[]
            e = []
            l = []
            for j in range(0,len(arr)):
                e.append(data[arr[j]])
                i.append(OutputImages[arr[j]])
                l.append(OutputLabelsNames[arr[j]])
            NewData.extend([e])
            NewImages.extend([i])
            NewLabels.extend([l])
        
        #Finding The mean of The Data Generated :
        mean = int(np.mean(numOfSamples))
        
        #Using my custom formula  of The Balance Process
        fb = max(numOfSamples) - min(numOfSamples) // (len(numOfSamples))
        #Adding 25% of number of Samples :
        fb = fb + (fb * 25 // 100)
        means = [fb,mean]

        #Difference between min and max of means list the compare it to deadNumOfData
        if max(means) - min(means) < deadNumOfData :
            balanceValue = max(means)

            #Verifying the balance value if it more than the max of numOfSamples :
            if balanceValue > max(numOfSamples):
                balanceValue = max(numOfSamples)

        #Or returning the min value of means list :
        else : 
            balanceValue = min(means)
        
        #Spliting the data into mutidimensional list for each className and images :
        for i in range(0,len(NewData)):
            if len(NewData[i]) > balanceValue :
                NewData[i] = NewData[i][:balanceValue]
                NewImages[i] = NewImages[i][:balanceValue]
                NewLabels[i] = NewLabels[i][:balanceValue]
        
            NewNumOfSamples.append(len(NewData[i]))
            for j in range(0,len(NewData[i])):
                ReturnedImages.append(NewImages[i][j])
                ReturnedLabels.append(NewLabels[i][j])
                ReturnedLabelsEncoded.append(NewData[i][j])
        
        #Preparing class Names lisst for the visualisation :
        ClassNames = self.ClassData.copy()
        for cn in range(0,len(ClassNames)):
            ClassNames[cn] = ClassNames[cn][ClassNames[cn].rindex("/")+1:]

        #Plotting the data distibuation and the limit of data generated by the balance funcs :
        #The plotting will show if the display param is True.
        if display == True :
            
            #Plotting the actual numbers of of samples and drow the limitation generated:
            plt.figure()
            plt.bar(ClassNames, numOfSamples,width=0.03)
            plt.plot((np.min(data),np.max(data)),(balanceValue,balanceValue),color="r")
            plt.title("Number of Images for each Class Detected.")
            plt.xlabel("Labels")
            plt.ylabel("Number of Images")
            plt.show()
            
            #plotting the generated Data with the limitaion of data:
            plt.figure()
            plt.bar(ClassNames, NewNumOfSamples,width=0.03)
            plt.plot((np.min(data),np.max(data)),(balanceValue,balanceValue),color="r")
            plt.title("Number of Images for the Balanced classes.")
            plt.xlabel("Labels")
            plt.ylabel("Number of Images")
            plt.show()
        
        print("balance value generated :",balanceValue)
        print("total images Extarcted from the Balance Data :",len(ReturnedImages),"\n")

        #adding number of classes and images imported to dataTypeInformations dict:
        self.dataTypeInformations["TotalImages"] = len(ReturnedImages)                       
        self.dataTypeInformations["TotalLabelsList"] = len(ReturnedLabels)

        #adding number of classes and images imported to LabelsExtracted dict:
        self.LabelsExtracted["LabelsEncoded"] = ReturnedLabelsEncoded
        self.LabelsExtracted["Labels"] = ReturnedLabels
        
        #Returning the NewData generated:
        return ReturnedImages, ReturnedLabels, ReturnedLabelsEncoded

    def SaveData(self,
                pathToData:str,
                ImagesCropped:list,
                LabelsNames:list):
                
        #checking the existance of the path to save data
        
        if os.path.isdir(pathToData) == False :
            #creating the save folder:
            os.mkdir(pathToData)

        #Removing the Last Data and generate new one :
        else:
            shutil.rmtree(pathToData)
            os.mkdir(pathToData)

        #creating the folders of different classes:
        for name in range(0,self.dataTypeInformations["NoOfClasses"]):
            FolderName = self.ClassData[name][self.ClassData[name].rindex("/")+1:]
            p = os.path.join(pathToData,FolderName)
            p = self.PathCorrector(p)
            os.mkdir(p)
        
        #Saving images from the data reutned by the DataExtarcting:
        for i in tqdm(range(0,len(ImagesCropped))):
            image = (ImagesCropped[i])
            newPath = os.path.join(pathToData,LabelsNames[i])
            newPath = self.PathCorrector(newPath)
            FileName = os.path.join(newPath,str(time.time()))+".png"
            FileName = self.PathCorrector(FileName)
            cv2.imwrite(FileName, image)