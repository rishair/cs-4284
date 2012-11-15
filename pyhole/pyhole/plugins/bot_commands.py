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
        (hash, message) = self.extract_command(kwargs)
        self.irc.reply(hash, str(random.randint(0, 10)))

