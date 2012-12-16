"""Summary Test Plugin"""

import commands
import socket
import random

from pyhole import irc
from pyhole import plugin
from pyhole import utils



class BotCommands(plugin.Plugin):
    """Tests the client-side summary"""

    @plugin.hook_add_command("bot")
    def bot(self, params=None, **kwargs):
        """Test out the server-side summary using non-local sending"""
        self.irc.reply(str(random.randint(0, 10)))

    @plugin.hook_add_command("rank")
    def rank(self, params=None, **kwargs):
        self.irc.reply(str(self.irc.rank))

