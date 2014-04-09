
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
    
    def __init__(self, line):
        try:
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
            self.sender = reg_match.groups()
            #syntax:
            # [nick/server name, username, hostname]
        else:
            self.sender = None
            
    def __bool__(self):
        return self._valid
        