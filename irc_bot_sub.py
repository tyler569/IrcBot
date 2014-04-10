#!/usr/bin/python3

'''
Socket-level IRC Bot in Python

Initially built for use on the Open Redstone Engineers IRC Channel

Copyright (C) 2014, Tyler Philbick
All Rights Reserved
See COPYING for license information
'''

from irc_bot import IrcBot


class IrcBotSub(IrcBot):
    # Here Go Command Functions

    def add(self, sender, *args):
        '''Add n numbers and echo the result to the user'''
        
        if len(args) > 0:
            try:
                self.send(str(sum([int(a) for a in args])), sender)
            except(ValueError):
                self.send("All arguments of add must be numbers", sender)
        else:
            self.send("add requires one or more arguments", sender)
            
    def d2bin(self, sender, *args):
        '''Convert a whole number to binary and echo it back to the user'''
        
        if len(args) == 1:
            try:
                self.send(bin(int(args[0])), sender)
            except(ValueError):
                self.send("d2bin required one whole number as an argument")
        else:
            self.send("d2bin required one whole number as an argument")
            
    def add_commands(self):
        '''Adds commands to the parent object's command dictionary'''
        #I will be attempting to do this more automatically in future
        
        self.cmd_dict = {"add": self.add, "d2bin": self.d2bin}

def main():
    '''main'''
    
    #add sys.agrv support for changing input vars to IrcBot?
    bot = IrcBotSub()
    bot.add_commands()
    bot.autorun()

if __name__ == '__main__':
    main()