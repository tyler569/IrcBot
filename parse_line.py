
'''
Socket-level IRC Bot in Python

Initially built for use on the Open Redstone Engineers IRC Channel

Copyright (C) 2014, Tyler Philbick
All Rights Reserved
See COPYING for license information
'''

import re


class ParseLine(object):
    '''Parses the IRC server's messages into their components'''
    
    def __init__(self, line, cmd_char):
        try:
            #matcd line against standard IRC format
            #see http://calebdelnay.com/blog/2010/11/parsing-the-irc-message-format-as-a-client
            reg_match = \
                re.match("^(?::(\S+) )?(\S+)(?: (?!:)(.+?))?(?: :(.+))?$",
                    line)
            #print(reg_match.groups()) # - debug
            self.groups = reg_match.groups()
            self._valid = True
            #Parsed line syntax:
            # [prefix, command, parameters, trail]
        except(AttributeError):
            self.groups = None
            self._valid = False
        
        if self._valid and self.groups[0] is not None:
            reg_match = re.match("^(\S+?)(?:(?:!(\S+))?@(\S+))?$",
                self.groups[0])
            #print(reg_match.groups()) # - debug
            self.prefix = reg_match.groups()
            #syntax:
            # [nick/server name, username, hostname]
            
            if self.prefix[1] in serverUsers:
                #MC server bot sent the message
                reg_match = re.match("(\w+): (.+)", self.groups[3])
                if reg_match is not None:
                    #True if message was a chat
                    self.sender = self.prefix[2], reg_match.groups[0]
                    self.text = reg_match.groups[1]
                else:
                    #Person joining/leaving MC
                    pass
            else:
                #Not sent from MC
                self.sender = self.prefix[2]
                self.text = self.groups[3]
            
            if self.text[0] == cmd_char:
                reg_match = \
                    reg.match("(\w+) (?:(?:'(.*?)')|(?:\"(.*?)\")|(\w+))+",
                        self.text
                if reg_match is not None:
                    self.irc_cmd = reg_match[0]
                    if len(reg_match > 1):
                        self.irc_cmd_args = reg_match[1:]
                    else:
                        self.irc_cmd_args = []
            else:    
                self.irc_cmd = None
                
                
                (?:(?:'(.*?)')|(?:"(.*?)")|(\w+))+
                
        else:
            self.sender = None
            
        self.command = self.groups[1]
        self.params = self.groups[2]
            
    def __bool__(self):
        return self._valid
        