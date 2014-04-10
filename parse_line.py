
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
        server_users = ("OREBuild", "ORESchool")
        
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
        
        if (self._valid and self.groups[0] is not None
                and self.groups[3] is not None):
            reg_match = re.match("^(\S+?)(?:(?:!(\S+))?@(\S+))?$",
                self.groups[0])
            #print(reg_match.groups()) # - debug
            self.prefix = reg_match.groups()
            #syntax:
            # [nick/server name, username, hostname]
            print(self.groups, self.prefix)
            
            if self.prefix[0] in server_users:
                #MC server bot sent the message
                reg_match = re.match("(\w+): (.+)", self.groups[3])
                if reg_match is not None:
                    #True if message was a chat
                    match_array = reg_match.groups()
                    self.sender = self.prefix[0], match_array[0]
                    self.text = match_array[1]
                else:
                    #Person joining/leaving MC
                    self.sender = self.prefix[0]
                    self.text = self.groups[3]
            else:
                #Not sent from MC
                self.sender = self.prefix[0]
                self.text = self.groups[3]
            
            if self.text[0] == cmd_char:
                match_array = []
                reg_iter = re.finditer(
                    "(?:(?:'(.*?)')|(?:\"(.*?)\")|(\S+))+", self.text)
                #This match willreturn an iterator that will yield
                #0 to many matches - it will match any word on its
                #own or it will match entire quoted segments:
                #ex:
                #   The quick brown "fox jumped" 'over the'
                #would match to:
                #   ["The", "quick", "brown", "fox jumped", "over the"]
                #HOWEVER:
                #the reg_iter will return:
                #   (None, None, "The"), (None, None, "quick")
                #Here, I attempt to rectifiy this by filtering all values
                #evlautaing to False out:
                for i in reg_iter:
                    reg_match = i.groups()
                    match_array += list(filter(bool, reg_match))
                self.irc_cmd = match_array[0][1:]
                #[1:] filters the command char from the command
                if len(match_array) > 1:
                    self.irc_cmd_args = match_array[1:]
                else:
                    self.irc_cmd_args = []
            else:    
                self.irc_cmd = None
        else:
            self.sender = None
            self.text = None
            self.irc_cmd = None
            self.irc_cmd_args = None
            self.prefix = self.groups[0]
            
        self.command = self.groups[1]
        self.params = self.groups[2]
            
    def __bool__(self):
        return self._valid
        