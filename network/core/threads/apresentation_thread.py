#coding: utf-8

from threading import Thread

class apresentationThread(Thread):

    def __init__ (self, method, addressReceived, message):
          Thread.__init__(self)
          self.method = method
          self.addr = addressReceived
          self.message = message

    def run(self):
        self.method(self.addr, self.message)
