#!/usr/bin/env python

import socket
import SocketUtil

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
         # botSocket.connect((bot[0], bot0[1]))
         botSocket.connect((socket.gethostname(), 21800))
         SocketUtil.send(botSocket, self.MASTER_PASSPHRASE)
         SocketUtil.recieve(botSocket, len(self.BOT_PASSPHRASE))
         botSocket.close()

if __name__ == '__main__':
   master = Master()