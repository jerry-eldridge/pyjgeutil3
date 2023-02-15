from transformers import ViTFeatureExtractor as vfe
from transformers import ViTForImageClassification as vic
import requests
import cv2

import os
import fnmatch
import os.path
import time

import numpy as np

class Image2Text:
    def __init__(self):
        self.modeldir_fe = 'C:/_BigData/_huggingface_transformers/ImageClf/fe'
        self.modeldir_model = 'C:/_BigData/_huggingface_transformers/ImageClf/model'
        self.fe = None
        self.model = None
        self.thoughts = []
        self.im = None
        return
    def download(self):
        print("Downloading model... This will download HUGE file...")
        x = input("Enter '123123' to proceed else any other key to quit.")
        if x != '123123':
            return
        fe= vfe.from_pretrained('google/vit-base-patch16-224')
        fe.save_pretrained(self.modeldir_fe)
        model = vic.from_pretrained('google/vit-base-patch16-224')
        model.save_pretrained(self.modeldir_model)
        print("Model downloaded and saved to folder...")
        self.fe = fe
        self.model = model
        return
    def load(self):
        print("Assuming already downloaded...running model...")
        fe= vfe.from_pretrained(self.modeldir_fe)
        model = vic.from_pretrained(self.modeldir_model)
        self.fe = fe
        self.model = model
        return
    def jpg_files(self,folder):
        L = []
        for root, dire, files in os.walk(folder):
            for fn in fnmatch.filter(files, "*.jpg"):
                try:
                    root = root.replace('\\','/')
                    filename = root + '/' + fn
                    filename = filename.replace('//','/')
                    L.append(filename)
                except:
                    continue
        return L
    def readfn(self, fn):
        im = cv2.imread(fn,1)
        self.im = im.copy()
        return
    def recognize(self):
        im = self.im.copy()
        x = self.fe(images=im, return_tensors="pt")
        y = self.model(**x)
        logits = y.logits
        # model predicts one of the 1000 ImageNet classes
        i = logits.argmax(-1).item()
        c = self.model.config.id2label[i]
        self.thoughts.append(c)
        return c
    def camera_open(self,camid=0):
        self.camid = 0
        self.cam = cv2.VideoCapture(self.camid)
        print("camera ",self.camid," is opened?",
              self.cam.isOpened())
        im0 = None
        try:
            FF,image = self.cam.read()
            im = np.zeros((image.shape[0], image.shape[1], 3), np.uint8)
            im = image
        except:
            print("Error opening camera...")
            return
        self.im = im.copy()
        return
    def camera_read(self):
        im0 = None
        try:
            FF,image = self.cam.read()
            im = np.zeros((image.shape[0], image.shape[1], 3), np.uint8)
            im = image
        except:
            print("Error opening camera...")
            return
        self.im = im.copy()
        return
    def camera_close(self):
        self.cam.release()
        return
    def __del__(self):
        self.camera_close()
    def __str__(self):
        s = '. '.join(self.thoughts)
        return s
    def visualize(self,wn="result",ms=-1):
        im = self.im.copy()
        sh = im.shape
        height = sh[0]
        width = sh[1]
        aspect = width/(height+1)
        width_goal = 800
        height_goal = 500
        ratio1 = width_goal/(width+1)
        ratio2 = height_goal/(height+1)
        ratio = min(ratio1,ratio2)
        hh = int(height*ratio)
        ww = int(width*ratio)
        im2 = cv2.resize(im,(ww,hh))
        cv2.imshow(wn,im2)
        ch = cv2.waitKey(ms)
        return ch
    def close_visualize(self):
        cv2.destroyAllWindows()
        return
    
        
