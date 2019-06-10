#coding: utf-8

from threading import Thread

class simpleThread(Thread):

    def __init__ (self, method):
          Thread.__init__(self)
          self.method = method

    def run(self):
        self.method()
