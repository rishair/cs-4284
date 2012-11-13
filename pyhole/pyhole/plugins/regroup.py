"""Channel Regrouping Plugin"""

import commands
import socket

from pyhole import irc
from pyhole import plugin
from pyhole import utils



class SummaryTest(plugin.Plugin):
    """Tests the client-side summary"""

    @plugin.hook_add_command("ungroup")
    def ungroup(self, params=None, **kwargs):
        """Leaves all channels a bot is in except for all of the default channels channel"""
        
        toremove = list(self.irc.channels)
        for default in self.irc.default_channels:
            toremove.remove(default)
        
        for rem in toremove:
            self.irc.part_channel(rem)
        
        self.irc.reply("ungroup;%s;done" % (hash(kwargs["full_message"] + self.irc.source)))
    
    @plugin.hook_add_command("regroup")
    def regroup(self, params=None, **kwargs):
        """Regroups a bot based off a certain parameter"""
        
        split = params.split(" ", 1)
        dest = split[0]
        split = split[1].split("=")
        if split[0] == "host":
            # test to see if the parameter is contained in this bots hostname
            hostname = socket.gethostname()
            if split[1] in hostname:
                self.irc.join_channel(dest)
        
        # No reply in this case: the reply is joining the channel