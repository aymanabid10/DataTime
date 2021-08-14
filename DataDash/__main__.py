#Importing the Dependencies :
from flask import Flask, render_template, Response, request, make_response
import os
import sys
import json 
import argparse
from .camera import VideoCamera

#init a Flask application :
app = Flask(__name__ , static_folder='static')

#init Some Values that chnages during the execution :
c=0
fps = 0
state = False
path =""
label = ""
classNames = []
dataFound = []
Names = []

#Generating the paths given from the interface :
def PathGenerator(path):
    if "/" in path :

        #Cenverts the the path given to lists:
        paths = path.split("/")
        for i in range(0,len(paths)):
            #Checking the existance of the paths :
            if os.path.exists("/".join(paths[:i+1])) == False :
                #Create the path if False :
                os.mkdir("/".join(paths[:i+1]))
    else :
        #Checking the existance of the Simgle path :
        if os.path.exists(path)  == False :
            #Create the path if False :
            os.mkdir(path)

    #Appending the path to classNames list :
    classNames.append(path)

#In some Cases, Windows makes some Errors while Extracting paths so we can figure it out using this func :
def PathCorrector(p:str):
    if sys.platform == "win32":
        p = p.replace("\ "[0],"/")
    return p

#Creating the index page with a Decorator :
@app.route('/', methods=['GET','POST'])
def index():
    #Defining some vars as global vars :
    global c
    global path , state

    #Getting the Data From the inteface , Depends on some States :
    if request.method == "POST" :
        if request.form.get('start') == "Start recording":
            c = 1
            state = True
        elif request.form.get("stop") == "Stop Recording":
            c = 0
            state = False
        elif request.form.get("path") == "Submit your path" :
            if request.form["path_name"] != "":
                path = request.form["path_name"]

                if "\ "[0] in path :
                    #Path Corrector in case "\" in the path given :
                    path = PathCorrector(p=path)
                
                #Creating The path :
                PathGenerator(path=path)
        else :
            pass
    
    #Render all the process to the page.html template :
    return render_template('page.html')

#Extracting the image from the .camera libary :
def gen(camera):
    while True:
        #Setting the fps as global var to use it in such as functions :
        global fps
        #Extracting the frame and the FPS from camera instance :
        frame,fps = camera.get_frame(c=c,path=path)

        #Creating a generator of bytes to the frame extracted and Defining the content-type as image:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#Creating the video_feed page with a Decorator :
@app.route('/video_feed')
def video_feed():

    #Returning the camera feed from gen func as a response at the /video_feed link:
    return Response(gen(video_stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#Creating the index page with a Decorator :
@app.route('/data_json',methods=["GET","POST"])
def data():
    #Setting the label as global var
    global label

    #Defining some vars to be rendered to the our custom API :
    images = 0
    cn = 0
    imagesNames = []

    #Checking the existance of 0 val in the datafound list(Some errors depends to put an another num in the end of the list and this case is 0):
    if not(dataFound ==[]):
        if dataFound[-1] == 0 :
            dataFound.pop(-1)

    #Cheking if the path not empty:
    if path != "":
        for i in os.listdir(path):
            #Appending the class names :
            imagesNames.append(i)
            #Calculating the number of image found or recorded:
            images += 1

        #extracting the only label name:
        label = path[path.rindex("/")+1:]

        #Errors of appending the same label name , so we can figure it out like that :
        if not(label in Names) : 
            Names.append(label)
            dataFound.append(images)
        
        #Updating the number of images at the same ClassName : 
        dataFound[Names.index(label)] = images

    #appending the 0 val :
    dataFound.append(0)
    
    #Creating a dictionary to convert it into JSON Format :
    informations = {"path" : path,
                    "collected" : images,
                    "fps" : fps,
                    "images_names" : imagesNames,
                    "labels" :Names,
                    "data" : dataFound,
                    "state" : state,
                    "label" : label
                    }
    #Making a response to the /data_json link as JSON Format :
    response = make_response(json.dumps(informations))

    #Specifying the content-type as appliication/json type :
    response.content_type = 'application/json'
    #Returning the JSON Data :
    return response

def main():
    #Set up the video_stream  instance as global
    global video_stream
    
    #Using the argparse lib to make choice of the interactive Data given by the user:
    parser = argparse.ArgumentParser(prog="Show Informations",
                                    usage="""
                                    Provide Two arguments
                                    """,
                                    description="""
    --------------------------
    Description:

        Welcome To DataDash Intreface powered by DataTime
    --------------------------
                                    """,
                                    epilog="Copyrights @ Ayman Abid (link)",
                                    formatter_class=argparse.RawDescriptionHelpFormatter,
                                    add_help=True
                                    )
    parser.add_argument("service",
                        type=str,
                        help="Put Collector here as default to run the DashBoard server.",
                        metavar="DASHBOARD TYPE")

    parser.add_argument("--camera_index",
                        type=int,
                        help="Set your Camera Index [as default, the Camera index is 0].",
                        default=0,
                        required=False)

    parser.add_argument("--window_size",
                        type=int,
                        help="Set you window size (the ROI size) [as default the ROI size is 200 px]",
                        default=200,
                        required=False)

    arg = parser.parse_args()
    
    #if the service arg is equal to "Collector" so we can exucute the Dashboard :
    if arg.service == "Collector":
        video_stream = VideoCamera(cam_index=arg.camera_index,
                                    roi_size=arg.window_size)
        
        #Launch the Server as Defaut 127.0.0.1:5000 :
        app.run(host='127.0.0.1', 
                debug=True,
                port="5000")

if __name__ == '__main__':
    #Exucuting the main function :
    main()