#!/usr/bin/env python

import socket
import time
import SocketUtil

class Bot:
   EOF = '\n'
   MASTER_PASSPHRASE = 'gits#9sac'
   BOT_PASSPHRASE    = 'standalone'

   def __init__(self):
      print 'Initializing Bot...'

      # set up a socket as a server
      # used socket.gethostname() instead of localhost so that the socket
      # would be visible to the outside world
      self.serverSocket = socket.socket()
      self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.serverSocket.bind((socket.gethostname(), 21800))
      self.serverSocket.listen(1)
      print 'Socket created'

      # master connection
      self.master = None

      self.notAuthenticated = True

      # listen for master and perform authentication
      while self.notAuthenticated:
         (self.notAuthenticated, self.master) = self.listenForMaster()

      # send bot passphrase
      SocketUtil.send(self.master, self.BOT_PASSPHRASE)

      self.master.close()
      self.serverSocket.close()
      print 'Socket shut down'

   """
   Listen for master and handle requests.
   """
   def listenForMaster(self):
         # blocks until client connects
         print 'Listening for Master...'
         connection, address = self.serverSocket.accept()
         
         print 'Connected to Master: ' + str(address)

         print 'Receiving from Master...'

         recvdStr = SocketUtil.recieve(connection)

         # authenticate connection
         if recvdStr != self.MASTER_PASSPHRASE:
            # not master
            connection.close()
            print 'Stranger tried to connect!'
            return (False, None)

         # was master
         return (True, connection)

   def getCurrTime(self):
      return int(time.time() * 1000) # time in milliseconds

if __name__ == '__main__':
   bot = Bot()
