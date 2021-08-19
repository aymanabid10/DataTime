#Importing Some Dependencies :
import cv2 
import numpy as np 
import os
import pickle
import json
import sys

#Create the path Corrector cause the windows paths issues :
def pathCorrector(p):
    if sys.platform == "win32":
        p = p.replace("\ "[0],"/")
    return p

#Getting the Extract.py full path
path =__file__ 
path = pathCorrector(p=path)

#Slicing into the last DataTime index to change with the Generator.py libary which is not in the same libary :
path = path[:path.rindex("DataTime")]
path = os.path.join(path,"DataTime","ClassificationGen")
path = pathCorrector(p=path)

#Insert the path in the PYTHONPATH with sys libary :
sys.path.insert(0,path)

#Now we can Import the Generator.py Libary from diffrent directories :
from Generator import DataImageGenerator

#Creating the ExtractDataImages class with DataImageGenerator as extended class :
class ExtractDataImages(DataImageGenerator):
    def __init__(self,
                path:str,
                NewSize:tuple,
                Save:bool,
                output="Output",
                display=False):
                
        super().__init__(path)
        
        #Defining new object to extarct data from the DataImageGenerator class:
        self.display = display
        self.path = str(path)
        self.NewSize = NewSize
        self.Save = Save
        self.output = output
        self.outputImages = []
        self.OutputLabelsNames = []
        self.OutputLabelsEncoded =[]
        self.imagesPath =[]
        self.classNames = []
        self.dataFiles = ["Labels.p","Labels.json","BackupData.p"]

        print("\nWelcome to DataTime Libary : \n")
        
    def ExtractImages(self):

        #extracting Folders paths :
        self.imagesPath , self.classNames , self.imagesLabels = self.DataToArray()

        #verifying the Correct Load of the hole data paths and informations:
        verification = self.DataVerification(images_path=self.imagesPath,
                                                            class_names=self.classNames,
                                                            images_labels=self.imagesLabels)
        
        #verification condition must be True:
        if verification == True :
            
            #Generating the Own Data using the informations of image and via ccropped it and returning lists containing numpy arrays:
            self.outputImages, self.OutputLabelsNames = self.DataExtarction(images_path=self.imagesPath,
                                                                                        class_names=self.classNames,
                                                                                        images_labels=self.imagesLabels,
                                                                                        NewSize=self.NewSize)

            self.outputImages,self.OutputLabelsNames,self.OutputLabelsEncoded = self.GenerateBalanceValue(OutputImages=self.outputImages,
                                                                    OutputLabelsNames=self.OutputLabelsNames,
                                                                    OutputLabelsEncoded=self.LabelsExtracted["LabelsEncoded"],
                                                                    display=self.display)
            
            #creating the pickle & json Files to Backup the Data :

            with open(self.dataFiles[-1],"wb") as p :
                pickle.dump(self.outputImages, p)
                p.close()
            
            with open(self.dataFiles[0],"wb") as l :
                pickle.dump(self.LabelsExtracted, l)
                l.close()
            
            with open("ClassNames.p","wb") as c :
                path = self.ClassData
                pickle.dump(path, c)
                c.close()
            
            with open(self.dataFiles[1], "w") as j:
                json.dump(self.dataTypeInformations,j)
                j.close()

            #creating arguments using if statment to make the save option for users:
            if self.Save == True :
                print("Start Saving you Data...")
                self.SaveData(pathToData=self.output,
                                            ImagesCropped=self.outputImages,
                                            LabelsNames=self.OutputLabelsNames)
                print("Saving Process finished succesfully.")
                
        #retuning the final result of the images cropped and its class names lists :
        return self.outputImages, self.OutputLabelsNames, self.OutputLabelsEncoded

    def myCustomData(self):
        
        #Defining a var for verif of the File : 
        v = True
        dataFiles = self.dataFiles

        #Checking the existance of files generated :
        for i in range(0,len(dataFiles)):
            if os.path.exists(dataFiles[i]) == False:

                #if the data verif is False, a new Data generated and v return False val:
                self.outputImages, self.OutputLabelsNames, self.OutputLabelsEncoded = self.ExtractImages()
                v = False

        #Loading The Data from the backup files if v is True:
        if v == True:
            
            
            #Checking the existance of classNames.p file which is important to load the class Names :
            if os.path.exists("ClassNames.p") == True:

                det = pickle.load(open("ClassNames.p","rb"))
                self.ClassData = det.copy()

                #if the length od det more than 0, the data will loaded from backup files:
                if not(len(det)) == 0 :
                    for cn in range(0,len(det)):
                        det[cn] = det[cn][det[cn].rindex("/")+1:]
                    print("Backup Data CLasses Detected :",det)
                    
                    #Giving the user the choice of load from backup or generate a new data :
                    vrf = input("Would you Want to Load The BackUp Data(Y/n): ")
                    print("")

                    #if vrf equal yes, the data loaded from backup files:
                    if vrf.lower() == "y":

                        #Calling the LoadBackup func:
                        self.outputImages, self.OutputLabelsNames, self.OutputLabelsEncoded = self.LoadBackup()
                    
                    #Or generate a new Data:
                    else:
                        self.outputImages, self.OutputLabelsNames, self.OutputLabelsEncoded = self.ExtractImages()
                
                #Exceptions of such problems, the data will generated again:
                else:
                    self.outputImages, self.OutputLabelsNames, self.OutputLabelsEncoded = self.ExtractImages()
            else:
                self.outputImages, self.OutputLabelsNames, self.OutputLabelsEncoded = self.ExtractImages()
        print("Done.\n")
        
        #Return the Data loaded:
        return self.outputImages, self.OutputLabelsNames, self.OutputLabelsEncoded

    def LoadBackup(self):
        
        #Loading the data Generated from the backup files:
        self.outputImages = np.array(pickle.load(open(self.dataFiles[2],"rb")))
        self.LabelsExtracted = pickle.load(open(self.dataFiles[0],"rb"))
        self.dataTypeInformations = json.load(open(self.dataFiles[1],"r"))
        
        #Giving some attributes values from the Data loaded:
        self.OutputLabelsNames = self.LabelsExtracted["Labels"]
        self.OutputLabelsEncoded = self.LabelsExtracted["LabelsEncoded"]

        #creating arguments using if statment to make the save option for users:
        if self.Save == True :
            print("Start Saving you Data...")
            self.SaveData(pathToData=self.output,
                                        ImagesCropped=self.outputImages,
                                        LabelsNames=self.OutputLabelsNames)
            print("Saving Process finished succesfully.")
                
        return self.outputImages, self.OutputLabelsNames, self.OutputLabelsEncoded