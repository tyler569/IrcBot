#!/usr/bin/python3

'''
Socket-level IRC Bot in Python

Initially built for use on the Open Redstone Engineers IRC Channel

Copyright (C) 2014, Tyler Philbick
All Rights Reserved
See COPYING for license information
'''

#Credit to qwerasd205 for letting me look at a simalier program
#and gain insight and inspiration.

import socket

from parse_line import ParseLine


class IrcBot(object):
    '''IRC bot main class'''
    
    def __init__(self, host = "irc.freenode.net", port = 6667,
            channel = "#OREServerChat", nick = "tBot569",
            owner = "tyler569", my_host = "d.vms.pw", silent = False):
        '''Declarations and Definitions'''
        self.irc_hostname = host
        self.irc_port = port
        self.irc_channel = channel
        self.bot_nickname = nick
        self.bot_identity = nick
        self.bot_real_name = nick
        self.owner = owner
        self.owner_irc = owner
        self.my_hostname = my_host
        
        self.disable_send = silent

    def connect(self):
        '''Connects to the IRC server'''
        self.sock = socket.socket()
        target = (self.irc_hostname, self.irc_port)
        self.sock.connect(target)

        join = "NICK {}\r\nUSER {} HOST {} bla:{}\r\nJOIN {}\r\n"

        self.sock.send(join.format(self.bot_nickname, self.bot_identity,
            self.my_hostname, self.bot_real_name, self.irc_channel).encode())
        
    def parse(self, line):
        '''Parses the IRC server's messages into their components'''
        try:
            reg_match = \
                re.match("^(?::(\S+) )?(\S+)(?: (?!:)(.+?))?(?: :(.+))?$",  
                    line)
            #print(reg_match.groups()) # - debug
            return(reg_match.groups())
            #Parsed line syntax:
            # [prefix, command, parameters, trail]
        except(AttributeError):
            return False

    def send(self, message, target = None):
        '''Sends a message to the IRC server
        
        The message goes to whatever is specified in the
        second argument, defaulting to the channel the
        bot is in.  To PM a user, change this at call
        time to a string matching their IRC nickname'''
        
        #sets the target to the channel if no name provided
        #Cannot be done in def due to scope of "self"
        target = target or self.irc_channel
        
        if self.disable_send:
            return False
        send = ["PRIVMSG ", target, " :", message, "\r\n"]
        self.sock.send("".join(send).encode())
        print("-SEND: " + message + " --> " + target)
        
    def pong(self, pong_arg):
        '''Responds to IRC server pings'''
        pong = "PONG :" + pong_arg
        self.sock.send(pong.encode())
        print(pong)
        
    def read_lines(self, sock, recv_buffer = 4096, delim = "\r\n"):
        # https://synack.me/blog/using-python-tcp-sockets
        buffer = ""
        data = True
        while data:
            data = sock.recv(recv_buffer)
            buffer += data.decode()
            while buffer.find(delim) != -1:
                line, buffer = buffer.split(delim, 1)
                yield line
        return
        
    def loop(self):
        '''Main execution loop of the bot'''
        
        for t_line in self.read_lines(self.sock):
            # try:
                # t_line = b_line.decode()
            # except(UnicodeDecodeError):
                # print("ERROR - could not decode line")
                # #Add more usefulness to this error later
            print(t_line)
            line = ParseLine(t_line)
            if not line:
                continue
            if line.groups[1] == "PING":
                self.pong(line.groups[3])
            print(line.groups)
            print(line.sender)


        

            
def main():
    '''main'''
    #add sys.agrv support for changing input vars to IrcBot?
    bot = IrcBot(channel = "#tbottest")
    bot.connect()
    bot.loop()

if __name__ == '__main__':
    main()