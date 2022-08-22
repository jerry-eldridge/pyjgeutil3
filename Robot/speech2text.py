import torch
from transformers import Speech2TextProcessor as spt
from transformers import Speech2TextForConditionalGeneration as sptg

import numpy as np

import scipy.io.wavfile as wav
import scipy.interpolate as si

import sounddevice as sd

import random

import warnings

class Speech2Text:
    def __init__(self):
        self.modeldir_model = 'C:/_BigData/_huggingface_transformers/speech2txt/model'
        self.modeldir_proc = 'C:/_BigData/_huggingface_transformers/speech2txt/proc'
        self.model = None
        self.proc = None
        self.sig = None
        self.rate = 16000 # this must be 16000 for this
        self.thoughts = []
        return
    def download(self):
        print("Downloading model... This will download HUGE file...")
        x = input("Enter '123123' to proceed else any other key to quit.")
        if x != '123123':
            return
        model = sptg.from_pretrained('facebook/s2t-small-librispeech-asr')
        model.save_pretrained(self.modeldir_model)
        proc = spt.from_pretrained('facebook/s2t-small-librispeech-asr')
        proc.save_pretrained(self.modeldir_proc)
        print("Model downloaded and saved to folder...")
        self.model = model
        self.proc = proc
        return
    def load(self):
        print("Assuming already downloaded...running model...")
        model = sptg.from_pretrained(self.modeldir_model)
        proc = spt.from_pretrained(self.modeldir_proc)
        self.model = model
        self.proc = proc
        return
    def listen(self,secs=1):
        print("Listening for secs=",secs,"seconds")
        q = input("Enter to listen> ")
        rate = self.rate
        sig = sd.rec(int(secs*rate),samplerate=rate,
                 channels=2, dtype='float64')
        sd.wait()
        self.sig = sig
        self.rate = rate
        return
    def readfn(self,fn):
        (rate,sig) = wav.read(fn)
        new_rate = self.rate
        if new_rate != rate:
            dur = sig.shape[0]/rate
            t0 = np.linspace(0,dur,sig.shape[0])
            v = int(sig.shape[0]*new_rate/rate)
            t1 = np.linspace(0,dur,v)
            
            f = si.interp1d(t0, sig.T)
            sig2 = f(t1).T
        self.sig = sig2
        self.rate = new_rate
        return
    def recognize(self):
        rate = self.rate
        sig = self.sig
        if len(list(sig.shape))>1:
            if sig.shape[1] != 1:
                sig2 = sig[:,0] # use mono
        else:
            sig2 = sig.copy()
        txt = []
        # catch deprecated __floordiv__ warning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            x = self.proc(sig2,sampling_rate=rate,
                 return_tensors="pt")
            genid = self.model.generate(x["input_features"],
                attention_mask=x["attention_mask"])
            txt = self.proc.batch_decode(genid)
            warnings.simplefilter("default")

        for x in txt:
            self.thoughts.append(x)
        return txt
    def __str__(self):
        s = '. '.join(self.thoughts)
        return s

    
