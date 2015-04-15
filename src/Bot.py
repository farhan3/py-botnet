#!/usr/bin/env python

import socket
import time
import Util

class Bot:
   MASTER_PASSPHRASE = 'gits#9sac'
   BOT_PASSPHRASE    = 'standalone'

   def __init__(self):
      print 'Initializing Bot...'

      # set up a socket as a server
      # used socket.gethostname() instead of localhost so that the socket
      # would be visible to the outside world
      self.serverSocket = socket.socket()
      self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.serverSocket.bind((socket.gethostname(), 21801))
      self.serverSocket.listen(1)
      print 'Socket created'

      # master connection
      self.master = None

      self.notAuthenticated = True

      # listen for master and perform authentication
      while self.notAuthenticated:
         (self.notAuthenticated, self.master) = self.listenForMaster()

      # send bot passphrase
      Util.send(self.master, self.BOT_PASSPHRASE)

      cmd = Util.recieve(self.master)
      

      # send curr time
      currTimeStr = str(self.getCurrTime())
      print 'Sending current time: ' + str(int(time.time() * 1000))
      Util.send(self.master, currTimeStr)
      print 'Current time sent'

      atkTime = Util.recieve(self.master)

      print 'Going to attack at ' + atkTime

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

         print 'Authenticating Master...'

         recvdStr = Util.recieve(connection)

         # authenticate connection
         if recvdStr != self.MASTER_PASSPHRASE:
            # not master
            connection.close()
            print 'Stranger tried to connect!'
            return (True, None)

         # was master
         print 'Master Authenticated'

         return (False, connection)

   def getCurrTime(self):
      return int(time.time() * 1000) # time in milliseconds

if __name__ == '__main__':
   bot = Bot()
