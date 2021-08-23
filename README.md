# DataTime

**DataTime** is a 100% Tunisian python library based for image
 classifications data extraction tasks as well as for data
collection using an interactive and dynamic dashboard your can
launch it from a CLI command (built-in command) makes
powerfull images collected for machine and deep 
learning tasks in particular computer vision tasks.

## Our Features

#### 1. DataExtraction :
- *Introduction* :

image classification is one of thee most commun computer vision
tasks in Machine Learning but the problem is Finding a great 
image dataset with the best resolution and the shape of 
the object in the image can be smaller than the actual image 
that can't give us a great Detection with a lower accuracy.

- *Data Extraction* :

**DataTime** is capable of fixing this problem using
[the GoogleAPI Open Images]("https://storage.googleapis.com/openimages/web/index.html") 
used for object detection ,so **DataTime** takes all these 
images of the object detection and extract all the bounding boxes
by crop them to create a powerfull image classification dataset 
but not only that, **DataTime** is capable of generating what it 
ever your number data is and this is a good point of generating 
a BigData images.

- *Data Balance* :
 
The main purpose of **DataTime** is makes your data powerfull
because the most Important in Machine Learning and deep learning
tasks is the the power of the preprocessing level of you Data so
**DataTime** is capable of balancing your own data into many
mathematics formulas applied on your own data.

- *Data Backup process*

**DataTime** makes the Time of the developer valuable, so the 
generated data is backup into pickle files that ones that the 
developer rerun the scripts , **DataTime** gives him the choice 
to use the BackUp Data.

#### 2. DataCollector :

- *Introduction* :

Data Collection also is one of the most important things in 
Machine Learning & Deep Learning tasks, so we can fix that 
problem with **DataTime** using an interactive and dynamic 
dashboard which i developed and you can call it with an built-in
CLI command called ***DataDash*** that takes few arguments.

- *Features* :

***DataDash*** include the camera feed, images collected 
paths and names and a Data visualizer based on your own Data 
collected.

***DataDash*** collect images with a variable ROI with a shape 
set up by the Developer with an argument on CLI and save only the 
ROI part on the path Selected.

***DataDash*** put your collected data on a Real-Time bar visualizer
that you can check your Data Distrubution.

## Documentation

Don't forget to check our Online Website with a great API 
Documentation from [here](https://linktodocumentation)

## Installation

You can easily install **DataTime** with few command lines 
instructions:

if you are in in Linux/MacOS or you have already install git 
in Windows 

```bash
git clone https://github.com/aymanabid10/DataTime.git
cd DataTime
``` 
if you are in Windows and you don't have a GIT yet , you can 
install it from install it from our repository and then type 

```bash
cd DataTime-master
```

#### Options
In order to install **DataTime** , i suggest you have already
a Virtual environnement if you don't, you can use Anaconda or 
Virtualenv library

- Anaconda :

```bash
conda create -n <your-Virtual-env-name>
conda activate <your-Virtual-env-name>
```

- Virtualenv :

```bash
sudo pip install virtualenv
python -m venv <your-Virtual-env-name> 
source <your-Virtual-env-name>/bin/activate
```
#### Important 

and Finally you have to install **DataTime**

```bash
pip install .
```
Congratulations you have already install **DataTime** !!

## Data From the GoogleAPI OpenImages :

in order to install your own dataset yout can visit this repository
[here](https://github.com/EscVM/OIDv4_ToolKit) that uses the 
OIDv4_ToolKit by *Google*.


## Usage/Examples

#### 1. DataExtraction :

This example include all you have to do to extract your own Data,
only the few things about our library and the most important stuffs 
but if you want more explination about the usage you can visit our
[Online API Docs]("") 
also reading the docs is important because 
you have the instructions of the DataBackups process. 

Your Folder Tree have to be like that :

        └──Project/
            │   └──data/
            │        ├──className0/   
            │        │       ├── labels/
            │        │       │     ├── image0.txt   
            │        │       │     ├── image1.txt    
            │        │       │     ├── image2.txt
            │        │       │     ├── image3.txt
            │        │       │     ├── ...
            │        │       │     ├── ...
            │        │       │     └──imageX.txt
            │        │       │
            │        │       ├── image0.png   
            │        │       ├── image1.png    
            │        │       ├── image2.png
            │        │       ├── image3.png
            │        │       ├── ...
            │        │       ├── ...
            │        │       └──imageX.png
            │        │
            │        ├──className1/
            │        │       ├── labels/
            │        │       │     └── ... 
            │        │       └── ... 
            │        ├── ...
            │        │
            │        └──classNameX/
            │                ├── labels/
            │                │     └── ... 
            │                └── ... 
            ├── train.py
            └── ...


In train.py :

```python
from DataTime.Custom.Extract import ExtractDataImages

Extractor = ExtractDataImages(path="data",
                    NewSize=(64,64),
                    Save=False,
                    display=True)

Images, LabelsNames, LabelsEncoded = Extractor.myCustomData()
```

#### 2. DataCollector :

DataDash is CLI command used to launch the dynamic dashBoard

```bash
DataDash -h
```

or 

```bash
DataDash --help
```

Output :

```bash
usage:
                                    Provide Two arguments


    --------------------------
    Description:

        Welcome To DataDash Intreface powered by DataTime
    --------------------------


positional arguments:
  DASHBOARD TYPE        Put Collector here as default to run the DashBoard
                        server.

optional arguments:
  -h, --help            show this help message and exit
  --camera_index CAMERA_INDEX
                        Set your Camera Index [as default, the Camera index is
                        0].
  --window_size WINDOW_SIZE
                        Set you window size (the ROI size) [as default the ROI
                        size is 200 px]

Copyrights @ Ayman Abid (link)
```

To run the Server

```bash
DataDash Collector
```

To customize your usement conditions, you have the choice of selecting
the index of the camera via the arg `--camera_index` that set up as 
default  `0` but you can change it also the ROI Rectangle size via
the arg `--window_size` that set up as defaut `200` which mean the ROI
shape is `200x200`

```bash
DataDash Collector --camera_index 0 --window_size 200
```

The dashboard is Flask based so the Output be like :

```bash
 * Serving Flask app 'DataDash.__main__' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 142-583-878
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
#### Important

- if your Input path is not Valid on your machine,  Don't worry the program will create it automatically.

- we suggest to use a external Camera for the compilicated object.

- Internet Connection is important during the use of the **DataDash** because it uses some online JavaScript and css libraries.

## License

[Apache-2.0](""https://www.apache.org/licenses/LICENSE-2.0)