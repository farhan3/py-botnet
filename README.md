# Botnet
Simple Botnet to perform a DDoS attack

### Master.py
The Master class represents the Master to control the Bots in the Botnet.
The Master reads the Bot data from bots_list.txt and communicates with the
Bots. It tells each Bot when to attack the target and at what time. It also
takes into account any time difference between itself and the Bot(s) in 
order to ensure that all Bots attack exactly at the specified time.

### TargetServer.py
A dummy server, which listens for TCP connections on the specified port.

### Bot.py
The Bot class represents a Bot to be used in the Botnet.
The Bot runs on the specified port, and listens for the Master.
Once the Master has connected and is authenticated, the necessary 
data is exchanged between the Bot and Master, i.e. target host, port number,
when to attack and the difference between the Bot and Master (if any) 
