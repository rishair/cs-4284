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
        (message, hash) = self.irc.extract_command(kwargs["full_message"])
        self.irc.reply(str(random.randint(0, 10)), hash)

