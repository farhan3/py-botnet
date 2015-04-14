#!/usr/bin/env python

import socket


EOF = '\n'

"""
   Receive msg from the provided connection.
   The length of the msg can be specified if known, otherwise
   default is 2048 chars.
"""
def recieve(connection, MSGLEN = 2048):
   recvdStr = [] # stores received substrings
   recvdStrLen = 0 # keep track of how much of the msg is received

   # keep receiving data until MSGLEN is reached or EOF is found
   while recvdStrLen < MSGLEN:
      recvdSubstring = connection.recv(MSGLEN - recvdStrLen)
      # recvdSubstring = connection.recv(min(MSGLEN - recvdStrLen, 2048))

      # empty string signals connection was closed
      if recvdSubstring == '':
         break 

      # check received substring 
      left, middle, right = recvdSubstring.partition(EOF)
      if left == EOF: # first char is an EOF
         break
      elif middle == EOF: # found EOF, only use left substring
         recvdStr.append(left)
         break
      else: # no EOF, keep receiving until MSGNLEN is received 
         recvdStr.append(recvdSubstring)
         recvdStrLen += len(recvdSubstring)

   # return final string
   return ''.join(recvdStr)

"""
Send a msg to the provided connection.
"""
def send(connection, msg):
   connection.send(msg)

def getCurrTime(self):
   return int(time.time() * 1000) # time in milliseconds
