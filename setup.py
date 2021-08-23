from setuptools import setup

setup(
  include_package_data=True,
  name = 'DataTime',
  packages = ['DataTime','DataDash'], 
  version = '1.0.0',
  license='Apache-2.0', 
  description = 'TYPE YOUR DESCRIPTION HERE', 
  author = 'Ayman Abid',
  author_email = 'abidcssaymancss@gmail.com',
  url = '',
  download_url = 'https://github.com/aymanabid10/DataTime.git',
  
  entry_points = {
        'console_scripts': [
            'DataDash = DataDash.__main__:main'
        ]
    },
    
  keywords = ['DataTime',
             'datatime', 
             'data time',
             'data collection', 
             'image classification',
             "deep learning",
             "data management",
             "datasets",
             "dataset",
             "image dataset"],
  
  install_requires=[ 
          'opencv-python',
          'numpy',
          'tqdm',
          "matplotlib",
          "flask"

      ],
  classifiers=[
    'Development Status :: 3 - beta',
    'Intended Audience :: Developers',   
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License', 
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    
  ],
)