#coding: utf-8

from threading import Thread

class Th(Thread):

    def __init__ (self, method, arg):
          Thread.__init__(self)
          self.method = method
          self.arg = arg

    def run(self):
        self.method(self.arg)
