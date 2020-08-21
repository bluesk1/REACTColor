import csv
import matplotlib as mpl
mpl.use('TkAgg')
import time
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from cv2 import *
import PySimpleGUIWeb as sg
import shutil
import smtplib as smptlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import sys
from progress.bar import IncrementalBar

def graphicalInterface():

    sg.theme('LightBlue')
    layout = [  [sg.Text('Please enter the experiment values to begin')],
                [sg.Text('Reaction Time:'), sg.InputText()],
                [sg.Text('Frequency:'), sg.InputText()],
                [sg.Text('Directory of the \'tempfiles\' directory (create one if you cannot find one):'), sg.InputText()],
                [sg.Text('Reaction ID:'), sg.InputText()],
                [sg.Text('Email for result delivery:'), sg.InputText()],
                [sg.Button('Begin Experiment'), sg.Button('Cancel')] ]


    window = sg.Window('REACT 1.0.5', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Cancel'):
            break
        if event in (None, 'Begin Experiment'):
            l = str(values[0])
            n = str(values[1])
            pl = str(values[2])
            react_id = str(values[3])
            email_address = str(values[4])
            break

    window.close()

    return l, n, pl, react_id, email_address

def RGB_average(image):
        npixels = image.size[0]*image.size[1]
        cols = image.getcolors(npixels)
        sumofRGB = [(x[0]*x[1][0], x[0]*x[1][1], x[0]*x[1][2]) for x in cols]
        avg = tuple([sum(x)/npixels for x in zip(*sumofRGB)])
        return avg

def takePicture(i, pl, react_id, n, cap, writer):
    ret, frame = cap.read()
    file_name = str(i) + '.png'
    cv2.imwrite(file_name, frame)
    im = Image.open(r''+str(pl)+"/" + str(react_id) + '/' + str(file_name))
    # CROPPING OPTIMIZATION IS HERE
    width, height = im.size
    left = 150
    top = height / 4
    right = 400
    bottom = 3 * height / 4
    im1 = im.crop((left, top, right, bottom))
    file_name2 = str(i) + '_' + '2' + '.png'
    im1.save(file_name2, 'png')
    new_file = file_name.replace('.png', '')
    r, g, b = RGB_average(im1)
    writer.writerow([int(new_file) * n, r, g, b])
    time.sleep(n)

def postProcess(pl, react_id, email_address, l, n):
    df = pd.read_csv("final.csv")

    plt.title("Time v. Color Concentration")
    plt.plot(df['time'], df['r'], label="Red", color='red')
    plt.plot(df['time'], df['g'], label="Green", color='green')
    plt.plot(df['time'], df['b'], label="Blue", color='blue')
    plt.xlabel("Time")
    plt.ylabel("Color Concentration")
    plt.legend()
    plt.savefig("final_graph.png",bbox_inches="tight",dpi=300)

    os.chdir(pl)

    shutil.make_archive("Experiment_"+react_id, 'zip', react_id)
    try:
        sendEmail(email_address, react_id, l, n)
    except:
        print("Email option did not work. Don't worry your data is saved in the tempfiles folder")
    
def sendEmail(email_address, react_id, l, n):
    fromAddress = sys.argv[0]
    toAddress = email_address
    if fromAddress == "0":
        print("Email Option not selected. Data stored in tempfiles")
    elif "gmail" in fromAddress:
        subject = "Your requested results from REACT"
        body = "Please see attached. Thanks for using REACT. The reaction conditions were as follows.\nTime: " + str(l) + "\n" + "Frequency: " + str(n) + "\n" + "Process complete." 
        msg = MIMEMultipart()
        msg['From'] = fromAddress
        msg['To'] = toAddress
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain')) 
        fileName = "Experiment_"+react_id+".zip"
        attachment = open(fileName, "rb")
        mimeapp = MIMEBase('application', 'octet-stream')
        mimeapp.set_payload((attachment).read())
        encoders.encode_base64(mimeapp)
        mimeapp.add_header('Content-Disposition', "attachment; fileName= %s" % fileName)
        msg.attach(mimeapp)
        mailApp = smptlib.SMTP('smtp.gmail.com', 587)
        mailApp.starttls()
        mailApp.login(sys.argv[1], sys.argv[2])
        mainBody = msg.as_string()
        mailApp.sendmail(fromAddress, toAddress, mainBody)
        mailApp.quit()
    else:
        print("Gmail is the only email platform supported. Data stored in tempfiles")
def main():
    cap = VideoCapture(int(sys.argv[3]))

    l, n, pl, react_id, email_address = graphicalInterface()

    l = int(l)
    n = int(n)
    r = int(l / n)
    os.chdir(str(pl))
    os.mkdir(str(react_id))
    os.chdir(str(react_id))

    bar = IncrementalBar('Countdown', max = r)

    with open('final.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'r', 'g', 'b'])
        for i in range(r):
            takePicture(i, pl, react_id, n, cap, writer)
            bar.next()
    cap.release()

    postProcess(pl, react_id, email_address, l, n)
    plt.show()

if __name__ == "__main__":
    main()
