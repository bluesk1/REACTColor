import csv
import time
import pandas as pd
import plotly.graph_objects as go
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

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['time'], y=df['r'], name="Red", marker_color='rgba(240, 52, 52, 1)'))
    fig.add_trace(go.Scatter(x=df['time'], y=df['g'], name="Green", marker_color='rgba(30, 130, 76, 1)'))
    fig.add_trace(go.Scatter(x=df['time'], y=df['b'], name="Blue", marker_color='rgba(30, 139, 195, 1)'))
    fig.update_layout(title="Time v. Color Concentration", xaxis_title="Time", yaxis_title="Color Concentration")
    fig.write_image("final_graph.png")
    fig.show()

    os.chdir(pl)

    shutil.make_archive("Experiment_"+react_id, 'zip', react_id)
    sendEmail(email_address, react_id, l, n)

def sendEmail(email_address, react_id, l, n):
    fromAddress = sys.argv[0]
    toAddress = email_address
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

if __name__ == "__main__":
    main()