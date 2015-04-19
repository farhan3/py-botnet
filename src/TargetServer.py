#!/usr/bin/env python

import socket
import signal
import sys
import thread
import time
import datetime

filebusy = False;

def log(line):
   global filebusy

   while filebusy:
      time.sleep(0.5) # wait 500 ms

   filebusy = True
   with open('log.txt', 'a') as logFile:
      logFile.write(line + '\n')

   filebusy = False

class Server:
   def __init__(self):
      print 'Initializing Server...'

      signal.signal(signal.SIGINT, self.shutdown)

      # set up a socket as a server
      # used socket.gethostname() instead of localhost so that the socket
      # would be visible to the outside world
      self.serverSocket = socket.socket()
      self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.serverSocket.bind((socket.gethostname(), 8080))
      self.serverSocket.listen(1)
      print 'Server Socket created'

      while (True):
         connection, address = self.serverSocket.accept()
         logLine = 'Received connection request from ' + str(address) \
            + " at " + str(datetime.datetime.now())
         print logLine
         thread.start_new_thread(log, (logLine,))
         connection.close()

      self.shutdown(None, None)

   def shutdown(self, signum, frame):
      if hasattr(self, 'serverSocket') and self.serverSocket != None:
         self.serverSocket.close()

      print '\nServer socket shut down'
      print 'Server shut down'

      sys.exit(0)

if __name__ == '__main__':
   server = Server()
