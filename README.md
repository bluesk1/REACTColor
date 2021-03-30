For the latest and most accurate documentation please visit: https://bluesk1.github.io/REACTColor/
The README files are still updated with every major version release.
***
# ReactColor
Thanks for using ReactColor. You are using version 0.0.1. React color was based on:

1.  Team-Based Learning for Scientific Computing and Automated Experimentation: Visualization of Colored Reactions

    Santiago Vargas, Siavash Zamirpour, Shreya Menon, Arielle Rothman, Florian Häse, Teresa Tamayo-Mendoza, Jonathan Romero, Sukin Sim, Tim Menke, and Alán Aspuru-Guzik
    Journal of Chemical Education Article ASAP
    DOI: 10.1021/acs.jchemed.9b00603

The code is NOT the same. There are key differences:
-ALL images and graphs are stored as PNGs
-The final spreadsheet (RGB values) are stored as a CSV
-ALL images, graphs, and CSV are sent as an email (by your email, see below)

## Get Started (install using pip)

To begin, install REACTColor by following the steps below. 

1. Make sure you have python3 installed on your computer by running this code:
   `python3`
   if you see an undefined response, then that means you have not installed python.
2. Create a tempfiles directory, and keep note of the path to the directory
4. Then run this code:
   `pip install https://bluesk1.github.io/REACTColor/REACTColor-0.0.1-py3-none-any.whl`
## OPTION 1) Usage (using REACTLauncher)

1. Copy the path to the REACTLauncher (download from latest release)
2. Type `chmod +x path\to\REACTLauncher`
3. Tap twice on the REACTLauncher, and you can see REACT actively install (steps 1 and 2 do not have to be repeated ever again)

## OPTION 2) Usage (using commandline)

Create a folder on your computer and call it tempfiles. This is where REACT will store each experiment before emailing. Then, to start REACT enter the following code in your terminal: 

`$ python -m REACTColor email@example.com password webcamchannel`
OR
`$ REACTColor email@example.com password webcamchannel`

Of course, replace email@example.com with yours, and enter the password of that email. If you would not like to use email, type 0 for both email and password. It will produce an error, but all files from the experiment will be stored in the tempfiles directory.

The webcam channel is dependent on your computer, it is usually 0, or 1. Please try and check which one is correct, by looking at source images. 

## Using REACTColor

REACT takes a picture at specified intervals and stores it in the tempfiles directory. We use smptlib to email the directory, which contains the table, and the graph. The email will oiginate from the email you specify when you start REACT, see the Get Started section for more information.

