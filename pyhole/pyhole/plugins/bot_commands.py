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
        """Test out the client-side summary using non-local sending"""
        self.irc.bot_reply("on it", kwargs["full_message"])

