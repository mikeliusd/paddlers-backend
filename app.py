from datetime import timedelta
from email.mime import base
from webbrowser import get
from flask import Flask, Response, url_for
from paddlers import deploy
from skimage.io import imread, imsave
import os
import cv2
import numpy as np
import paddle
import paddlers as pdrs
from paddlers import transforms as T
from paddlers.tasks.utils.visualize import visualize_detection
from matplotlib import pyplot as plt
from PIL import Image
from flask import request
import base64
PROC_PROCESSING=1
PROC_PROCESSED=2
proc_id=-1
status=[]
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response
def setStatus(statusId,code):
    global status
    status[statusId]=code
    return
def diffRecongize(input1,input2,output,id):
    pretor = deploy.Predictor(model_dir=os.getcwd()+'/models/diffRecongize')
    result=pretor.predict(img_file=(input1,input2))
    imsave(output,result[0]["label_map"],check_contrast=False)
    img1=Image.open(output)
    img2=Image.open(input1)
    img2=img2.convert('RGBA')
    img1=img1.convert('RGBA')
    img=Image.blend(img1,img2,0.5)
    img.save(output)
    status[id]=True
def get_lut():
    lut = np.zeros((256,3), dtype=np.uint8)
    lut[0] = [255, 0, 0]
    lut[1] = [30, 255, 142]
    lut[2] = [60, 0, 255]
    lut[3] = [255, 222, 0]
    lut[4] = [0, 0, 0]
    return lut
def itemDiv(input1,output,id):
    pretor = deploy.Predictor(model_dir = os.getcwd()+'/models/itemDiv')
    inputImage = imread(input1,1) 
    inputImage = inputImage.astype(np.uint32)
    result=pretor.predict(img_file=input1)
    res=result["label_map"]
    lut=get_lut()
    r=np.array(list(map(lambda x:lut[x],res)))
    imsave(output,r,check_contrast=False)
    img1=Image.open(input1)
    img2=Image.open(output)
    img=Image.blend(img1,img2,0.5)
    img.save(output)
    status[id]=True
def targetExact(input1,output):
    pretor = deploy.Predictor(model_dir=os.getcwd()+'/models/targetExact')
    result=pretor.predict(img_file=input1)
    imsave(output,result["label_map"],check_contrast=False)
    img1 = Image.open(input1) 
    img2 = Image.open(output)
    img2=img2.convert('RGBA')
    img1=img1.convert('RGBA')
    img=Image.blend(img1,img2,0.5)
    img.save(output)
def targetRecongize(input1,id):
    pretor = deploy.Predictor(model_dir=os.getcwd()+'/models/targetRecongize')
    result=pretor.predict(img_file=(input1))
    visualize_detection(image=input1,result=result,save_dir=os.getcwd()+"/")
def img_base64(img):
    image=''
    with open(img,'rb') as imgF:
        image=imgF.read()
        image=base64.b64encode(image)
    return image
@app.route("/backend/process",methods=["GET","POST"])
def routeDiffRecongize():
    global proc_id
    if request.method=='POST':
        proc_id=proc_id+1
        f=request.files['image1']
        f.save(os.getcwd()+"/"+str(proc_id)+".png")
        status.append(False)
        type=request.args.get('type','')
        if type=='diffRecongize':
            f2=request.files['image2']
            f2.save(os.getcwd()+"/"+str(proc_id)+"_2.png")
            diffRecongize(os.getcwd()+"/"+str(proc_id)+".png",os.getcwd()+"/"+str(proc_id)+"_2.png",os.getcwd()+"/"+str(proc_id)+"_out.png",proc_id)
        elif type=='itemDiv':
            itemDiv(os.getcwd()+"/"+str(proc_id)+".png",os.getcwd()+"/"+str(proc_id)+"_out.png",proc_id)
        elif type=='targetExact':
            targetExact(os.getcwd()+"/"+str(proc_id)+".png",os.getcwd()+"/"+str(proc_id)+"_out.png")
        elif type=='targetRecongize':
            targetRecongize(os.getcwd()+"/"+str(proc_id)+".png",proc_id)
        return str(proc_id)
@app.route("/backend/getimage",methods=["GET","POST"])
def getimage():
    if(request.args.get('type','')!="targetRecongize"):
        return img_base64(os.getcwd()+"/"+request.args.get('id','')+"_out.png")
    else:
        return img_base64(os.getcwd()+"/visualize_"+request.args.get('id','')+".png")

        #return img_base64(os.getcwd()+"/"+request.args.get('id','')+".png")