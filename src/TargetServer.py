#!/usr/bin/env python

import socket
import signal
import sys
import threading
import time
import datetime
import SocketServer
import Util

filebusy = False;

def log(line):
   global filebusy

   while filebusy:
      time.sleep(0.5) # wait 500 ms

   filebusy = True
   with open('log.txt', 'a') as logFile:
      logFile.write(line + '\n')

   filebusy = False

def shutdown(signum, frame):
   server.shutdown()
   print '\nServer shut down'

   sys.exit(0)

class ClientRequestHandler(SocketServer.BaseRequestHandler):
   def handle(self):

      logLine = 'Received connection request from ' + \
         str(self.client_address) + 'at ' + str(datetime.datetime.now())
      print logLine

      log(logLine)

      while True:
         try:
            rcvdStr = Util.recieve(self.request)

            if len(rcvdStr) < 1:
               break

            print rcvdStr

            log(rcvdStr)
         except socket.error as msg:
            log(str(msg))
            break


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
   pass

if __name__ == '__main__':
   print 'Initializing Server...'

   signal.signal(signal.SIGINT, shutdown)

   HOST, PORT = socket.gethostname(), 8081

   server = ThreadedTCPServer((HOST, PORT), ClientRequestHandler)
   server.allow_reuse_address
   ip, port = server.server_address

   # Start a thread with the server -- that thread will then start one
   # more thread for each request
   serverThread = threading.Thread(target=server.serve_forever)
   # Exit the server thread when the main thread terminates
   serverThread.daemon = True
   serverThread.start()
   print 'Server is listening in thread:', serverThread.name
   print 'Use Ctrl+C to stop server'

   while True:
      time.sleep(60)
