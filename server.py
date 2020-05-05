#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
import os
import atexit
import serial
import cv2, time,sys
import numpy as np

app = Flask(__name__)
api = Api(app)


def exit_handler():
    None #fa cose se il programma viene interrotto


@app.route("/video", methods=["GET"])
def test():
    img = start(0,0)
    return str(im)

def altre(base):
    inverted = cv2.bitwise_not(base) #immagine invertita
    gray = cv2.cvtColor(base,cv2.COLOR_BGR2GRAY)#trasforma da BGR (volorata) a scala di grigi

    return inverted,gray

def resize(base,scale):
    scale_percent = 100+scale # percent of original size
    width = int(base.shape[1] * scale_percent / 100)
    height = int(base.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    return cv2.resize(base, dim, interpolation = cv2.INTER_AREA)

def reticolo(base,dim,coordinate,thickness):
    t = thickness
    x = dim[0]
    y = dim[1]
    inizio = coordinate[0]/100
    fine = coordinate[1] /100
    tmp = cv2.line(base, (int(x/2),int(y/2 - y*inizio)), (int(x/2),int(y/2 - y*fine)), (0,0,255),t)#sopra
    tmp = cv2.line(base, (int(x/2),int(y/2 + y*inizio)), (int(x/2),int(y/2 + y*fine)), (0,0,255),t)#sotto

    tmp = cv2.line(base, (int(x/2 - x*inizio),int(y/2)),(int(x/2 - x*fine),int(y/2)), (0,0,255),t)#destra
    tmp = cv2.line(base, (int(x/2 + x*inizio),int(y/2)),(int(x/2 + x*fine),int(y/2)), (0,0,255),t)#sinistra

    return tmp

def start(camera_index,scale_factor):
    video = cv2.VideoCapture(camera_index) #zero e' l'indice della videocamera, 1 se la seconda collegata e cosi via

    while True:
        check,base = video.read()#prende l'immagine base dalla camera

        base = resize(base,scale_factor)#ridimensiona l'immagine, prende <immagine di partenza>,<quanto deve ridimensionarla> (-50 dimezza la dimensione)
        inverted,gray = altre(base) #crea due immagini con colori differenti della base

        coordi = (30,10)#inizio,fine reticolo

        dim = (base.shape[1],base.shape[0])#dimensioni dell'immagine una volta ridimensionata <x>,<y>
        img = reticolo(base,dim,coordi,3) #<img>, <dimensioni img>, <%da cui partire con le righe(50 è il max perchè parte da metà img)>, <%dove finire>, <spessore>
        None                             #(base,dim,30,10,3) le righe partiranno dal 30% di distanza dal centro e finiranno al 10% di distanza dal centro


        gray = reticolo(gray,dim,coordi,3)
        inverted = reticolo(inverted,dim,coordi,3)

        #cv2.imshow("Torretta Della Morte_Gray",gray)
        #cv2.imshow("Torretta Della Morte_Negative",inverted)
        #cv2.imshow("Torretta Della Morte_Normal",img)# mostra l'immagine e dà il nome alla finestra
        video.release() #rilascia i processi legati alla videocamera
        return img


if __name__ == '__main__':
     app.run(host='0.0.0.0',debug = True)
     atexit.register(exit_handler)
