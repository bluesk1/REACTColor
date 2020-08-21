import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE/"README.md").read_text()

setup(
   name="REACTColor", 
   version="0.0.1", 
   descp="REACTColor can be used to monitor colorimetric reactions.", 
   long_descp=README,
   long_descp_content="text/markdown", 
   author="Saathvik Kannan", 
   license="MIT", 
   classifiers=[ 
        "License :: OSI Approved :: MIT License", 
        "Programming Language :: Python :: 3", 
        "Programming Language :: Python :: 3.7", 
   ], 
   packages=["REACTColor"], 
   includepackagedata=True, 
   installrequires=["pandas","matplotlib", "Pillow", "opencv-python", "PySimpleGUIWeb","progress"], 
   entrypoints={ 
       "console_scripts":[ 
           "REACTColor=REACTColor.__main__:main", 
       ] 
   }, 
 ) 
