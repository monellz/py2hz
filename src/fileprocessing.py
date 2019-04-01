from interface import AbstractFileProcessing
import os
import json
import pickle

class Updator(AbstractFileProcessing):
    '''update probability file'''
    def __init__(self,src,dst):
        self.src = src
        self.dst = dst
    def process(self):
        with open(self.src,"rb") as f:
            src_objs = pickle.load(f)
        try:
            f = open(self.dst,"rb")
        except FileNotFoundError:
            f = open(self.dst,"wb")
        
        

class Officialfpcs(AbstractFileProcessing):
    '''
        2016-xx.txt
        generate trans.pkl emit.pkl start.pkl
        n-gram
    '''
    def __init__(self):
        self.encoding = 'gb18030'
        self.fns = ['2016-02.txt','2016-04.txt','2016-05.txt','2016-06.txt','2016-07.txt','2016-08.txt','2016-09.txt','2016-10.txt','2016-11.txt']
        
        #pkl
        self.rmode = "rb"
        self.wmode = "wb"
    def hhm_1(self):
        '''1 order hhm '''
        for fn in self.fns:
            name = self.absaddr(fn)
            with open(name,"r",encoding = self.encoding) as f:
                objs = f.read().split('\n')
            objs.pop()
            objs = [json.loads(obj) for obj in objs]
            name = self.absaddr(fn)
            f = self.openfile("trans-1-n.pickle",self.rmode,self.wmode)
            
            
            
            
        
    def process(self):
        pass