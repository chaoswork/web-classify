#coding=utf-8

# 记录员:记录工作流程中的一些信息
class Recorder:
    __info = None               # 静态变量
    def __init__(self):
        if self.__class__.__info is None:
            self.__class__.__info = ''
        
    def write(self,string):
        self.__class__.__info += string

    def read(self):
        return self.__class__.__info
    
    def reset(self):
        self.__class__.__info = ''
