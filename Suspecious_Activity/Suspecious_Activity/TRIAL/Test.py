"""
import requests
import json
location_req_url='http://api.ipstack.com/103.51.95.183?access_key=fcdaeccb61637a12fdf64626569efab0'

import tkinter as tk
from tkinter.filedialog import askopenfilename
import os
# import sys
from PIL import Image, ImageTk
import PIL.Image
import cv2
import tflearn
import numpy as np
import tensorflow as tf
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression


import warnings
warnings.filterwarnings('ignore') # suppress import warnings



root=tk.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.configure(background="cyan3")

root.title(" "*190+"---SUSPECIOUS ACTIVITY DETECTION---")


IMG_SIZE = 50
LR = 1e-3

MODEL_NAME = 'VIOLENCE-{}-{}.model'.format(LR, '2conv-basic')

tf.logging.set_verbosity(tf.logging.ERROR) # suppress keep_dims warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # suppress tensorflow gpu logs





def MAIL(d_msg):
    #def Send():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    
    
    
    msg = MIMEMultipart()
    fromaddr = 'omkar0.srccode@gmail.com'
    toaddr = 'omkar0.srccode@gmail.com'
    msg['From'] = fromaddr
    msg['To'] = toaddr
    password = 'Omkar@123'
    msg['Subject']='Violence Alert'
    
    
    r = requests.get(location_req_url)
    location_obj = json.loads(r.text)
    
    location2 = "%s, %s" % (location_obj['city'], location_obj['region_code'])
    print(location2)
    
    body = d_msg+' Violence probability at '+str(location2)+' is Detected.'
    msg.attach(MIMEText(body,'plain'))
    s=smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    try:
        s.login(fromaddr,password)
        text = msg.as_string()
        s.sendmail(fromaddr,toaddr,text)
        print('Mail Sent Successfully!!!!')
    except (smtplib.SMTPException,ConnectionRefusedError,OSError):
        print('Oops Mail Not Sent!!!')




def openphoto():
    #dirPath = "test/test"
    #fileList = os.listdir(dirPath)
    # for fileName in fileList:
    #     os.remove(dirPath + "/" + fileName)
    #P_th = 'F:/project/breath_detection/breath_project/train/train'
    fileName = askopenfilename( title='Select image for analysis ',
                              filetypes=[('All files', '*.*'), ('image files', '.jpeg')])

    

    load = PIL.Image.open(fileName)
    render = ImageTk.PhotoImage(load)
    img = tk.Label(root, image=render, height="250", width="500",bg="cyan3")
    img.image = render
    img.place(x=350, y=10)




"""
#    gs = cv2.cvtColor(cv2.imread(imgpath, 1), cv2.COLOR_RGB2GRAY)
#    x1 = int(gs.shape[0] / 2)
#    y1 = int(gs.shape[1] / 2)
#
#    gs = cv2.resize(gs, (x1, y1))
#
#    retval, threshold = cv2.threshold(gs, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
"""

    f=fileName.split("/").pop()
    f=f.split(".").pop(0)
    print(fileName)
    print(f)
    filepath=fileName

    def process_verify_data(filepath):

        verifying_data = []

        img_name = filepath.split('.')[0]
        img = cv2.imread(filepath, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        verifying_data = [np.array(img), img_name]

        #np.save('verify_data.npy', verifying_data)
        np.save('verify_data - Copy.npy', verifying_data)
        

        return verifying_data

    def analysis(filepath):

        verify_data = process_verify_data(filepath)

        str_label = "Cannot make a prediction."
        status = "Error"

        tf.reset_default_graph()

        convnet = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 3], name='input')

        convnet = conv_2d(convnet, 32, 3, activation='relu')
        convnet = max_pool_2d(convnet, 3)

        convnet = conv_2d(convnet, 64, 3, activation='relu')
        convnet = max_pool_2d(convnet, 3)

        convnet = conv_2d(convnet, 128, 3, activation='relu')
        convnet = max_pool_2d(convnet, 3)

        convnet = conv_2d(convnet, 32, 3, activation='relu')
        convnet = max_pool_2d(convnet, 3)

        convnet = conv_2d(convnet, 64, 3, activation='relu')
        convnet = max_pool_2d(convnet, 3)

        convnet = fully_connected(convnet, 1024, activation='relu')
        convnet = dropout(convnet, 0.8)

        convnet = fully_connected(convnet, 4, activation='softmax')
        convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy',
                             name='targets')

        model = tflearn.DNN(convnet, tensorboard_dir='log')


        if os.path.exists('{}.meta'.format(MODEL_NAME)):
            model.load(MODEL_NAME)
            print('Model loaded successfully.')
#            load=tk.Label(root,text="Model Loaded Successfully",width=30,height=2,font=("Tempus Sans ITC", 13, "bold"),background="red",foreground="white")
#            load.place(x=450,y=455)
        else:
            print('Error: Create a model using neural_network.py first.')
#            Uload=tk.Label(root,text='Error: Create a model using neural_network.py first.',width=30,height=2,font=("Tempus Sans ITC", 13, "bold"),background="red",foreground="white")
#            Uload.place(x=450,y=455)
        img_data, img_name = verify_data[0], verify_data[1]

        orig = img_data
        data = img_data.reshape(IMG_SIZE, IMG_SIZE, 3)


        
        model_out = model.predict([data])[0]
        print(np.argmax(model_out))
        if np.argmax(model_out) == 0:
            str_label = 'CROWD'
        elif np.argmax(model_out) == 1:
            str_label = 'FIGHT'
        elif np.argmax(model_out) == 2:
            str_label = 'GUNS'
        elif np.argmax(model_out) == 3:
            str_label = 'KNIVES'

        #if str_label == 'Healthy':
         #   status = 'Healthy'
        #else:
        
        if str_label=='CROWD':
            
            result=tk.Label(root,text="Normal Crowd is noticed",width=20,height=2,font=("Tempus Sans ITC",25,"bold"),background="cyan3",foreground="green")
            result.place(x=400,y=500)
            
        
        if str_label=='FIGHT':
            
            result=tk.Label(root,text="!!! Street Fighting is Noticed !!!",width=35,height=2,font=("Tempus Sans ITC",25,"bold"),background="cyan3",foreground="red")
            result.place(x=360,y=500)
            #d_msg = 
            MAIL("!!! Street Fighting is Noticed !!!")
            
        if str_label=='GUNS':
            
            result=tk.Label(root,text="!!! Gun is Detected, kindly look into it !!!",width=35,height=2,font=("Tempus Sans ITC",25,"bold"),background="cyan3",foreground="red")
            result.place(x=360,y=500)
            MAIL("!!! Gun is detected !!!")
        
        if str_label=='KNIVES':
            
            result=tk.Label(root,text="!!! Knife is Detected, kindly look into it !!!",width=35,height=2,font=("Tempus Sans ITC",25,"bold"),background="cyan3",foreground="red")
            result.place(x=360,y=500)
            MAIL("!!! Knife is detected !!!")
        
        print(str_label)

        
        
        
        return str_label
    
    
    

    analysis(filepath)


def KILL():
    root.destroy()
    

button1 = tk.Button(root, text="Browse Photo", command = openphoto,width=30,height=2,font=("Tempus Sans ITC", 13, "bold"),background="green")
button1.grid(column=0, row=1, padx=10, pady = 10)
button1.place(x=450,y=400)


exit =  tk.Button(root, text="Exit", command = KILL,width=30,height=2,font=("Tempus Sans ITC", 13, "bold"),background="red")
exit.place(x=450,y=600)




root.mainloop()



"""









import warnings
warnings.filterwarnings('ignore') # suppress import warnings

import os
import sys
import cv2
import tflearn
import numpy as np
import tensorflow as tf
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression

''' <global actions> '''

IMG_SIZE = 100
LR = 1e-3
MODEL_NAME = 'VIOLENCE-{}-{}.model'.format(LR, '2conv-basic')
tf.logging.set_verbosity(tf.logging.ERROR) # suppress keep_dims warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # suppress tensorflow gpu logs

''' </global actions> '''

def process_verify_data(filepath):

    verifying_data = []

    img_name = filepath.split('.')[0]
    img = cv2.imread(filepath, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    verifying_data = [np.array(img), img_name]
    
    np.save('verify_data.npy', verifying_data)
    
    return verifying_data

def analysis(filepath):

    verify_data = process_verify_data(filepath)

    str_label = "Cannot make a prediction."
    status = "Error"

    tf.reset_default_graph()

    convnet = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 3], name='input')


    convnet = conv_2d(convnet, 32, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 64, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 128, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 32, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = conv_2d(convnet, 64, 3, activation='relu')
    convnet = max_pool_2d(convnet, 3)

    convnet = fully_connected(convnet, 1024, activation='relu')
    convnet = dropout(convnet, 0.8)
    
    convnet = fully_connected(convnet, 2, activation='softmax') #No. of Classes
    convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

    model = tflearn.DNN(convnet, tensorboard_dir='log')
    """
    if os.path.exists('{}.meta'.format(MODEL_NAME)):
        model.load(MODEL_NAME)
        print ('Model loaded successfully.')
    else:
        print ('Error: Create a model using neural_network.py first.')
    """
    img_data, img_name = verify_data[0], verify_data[1]

    orig = img_data
    data = img_data.reshape(IMG_SIZE, IMG_SIZE, 3)

    model_out = model.predict([data])[0]

    if np.argmax(model_out) == 0: str_label = 'CROWD'
    elif np.argmax(model_out) == 1: str_label = 'FIGHT'
    elif np.argmax(model_out) == 2: str_label = 'GUN'
    elif np.argmax(model_out) == 3: str_label = 'KNIFE'

    #if str_label =='Healthy': status = 'Healthy'
    #else: status = 'Unhealthy'

    result = str_label
    
    #if (str_label != 'Healthy'): result += '\nDisease: ' + str_label + '.'

    return result

def main():
    #def Send():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture("E:\Suspecious_Activity\Bruce_Lee_Trim.mp4")
    while True:
        msg = MIMEMultipart()
        fromaddr = 'omkar0.srccode@gmail.com'
        toaddr = 'omkar0.srccode@gmail.com'
        msg['From'] = fromaddr
        msg['To'] = toaddr
        password = 'Omkar@123'
        msg['Subject']='Location'
        
        
        ret , frame = cap.read()
        
        cv2.imwrite('E:/Suspecious_Activity/img1.jpg',frame)
        fileName = 'E:/Suspecious_Activity/img1.jpg'
#    fileName = askopenfilename(initialdir='/dataset', title='Select image for analysis ',
#                                       filetypes=[("all files", "*.*")])
        print(fileName)
        #print (analysis(fileName))
        result = analysis(fileName)
        print(result)
        cv2.putText(frame,str(result),(30, 450), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0))
        mob = cv2.imread('E:/Suspecious_Activity/img1.jpg')
        cv2.imshow('frame',mob)
        """
        r = requests.get(location_req_url)
        location_obj = json.loads(r.text)
        
        location2 = "%s, %s" % (location_obj['city'], location_obj['region_code'])
        print(location2)
        body = 'Location of ROBOT IS '+str(location2)+" "+str(result)+' Detected.'
        msg.attach(MIMEText(body,'plain'))
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()"""
        """
        try:
            s.login(fromaddr,password)
            text = msg.as_string()
            s.sendmail(fromaddr,toaddr,text)
            print('Mail Sent Successfully!!!!')
        except (smtplib.SMTPException,ConnectionRefusedError,OSError):
            print('Oops Mail Not Sent!!!')"""
        cv2.putText(frame,str(result),(30, 450), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 0))
        
        if cv2.waitKey(1)==ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
#def Repeat():
#   from subprocess import call
#   call(["python","Output Script.py"])

if __name__ == '__main__':
    main()
    #Repeat()
    
    
    
    
    
    
    
    
    
    
    
#==============================================================================
    
