
"""Load plugin"""

from pyhole import plugin
import time

class TestLoad(plugin.Plugin):
    """Used to test how many plugins actually update with an update command"""

    @plugin.hook_add_command("load")
    def load(self, params=None, **kwargs):
        """Creates artificial load"""
        
        p = params.split(" ")
        if not len(p) == 3:
            self.irc.reply("Usage: .load [message size] [send count] [Delay between sends in seconds (accepts floating points)]")
        
        #simulate data
        data = '0' * int(p[0])
        for it in range(int(p[1])):
            self.irc.reply(data)
            time.sleep(float(p[2]))
        
        self.irc.reply("load;%s;done" % (hash(kwargs["full_message"] + self.irc.source))
