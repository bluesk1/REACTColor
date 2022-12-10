import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE/"README.md").read_text()

setup(
   name="REACTColor", 
   version="0.0.2", 
   descp="REACTColor can be used to monitor colorimetric reactions.", 
   long_descp=README,
   long_descp_content="text/markdown", 
   long_description=README,
   long_description_content_type='text/markdown',
   author="Saathvik Kannan", 
   license="MIT", 
   classifiers=[ 
        "License :: OSI Approved :: MIT License", 
        "Programming Language :: Python :: 3", 
        "Programming Language :: Python :: 3.7", 
   ], 
   packages=["REACTColor"], 
   includepackagedata=True, 
   install_requires=["pandas","matplotlib", "Pillow", "opencv-python", "PySimpleGUIWeb","progress"], 
   entry_points={ 
       "console_scripts":[ 
           "REACTColor=REACTColor.__main__:main", 
       ] 
   }, 
 ) 
