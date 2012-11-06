"""Summary Test Plugin"""

import commands
import socket
import random

from pyhole import irc
from pyhole import plugin
from pyhole import utils



class Summarizer(plugin.Plugin):
    """Tests the client-side summary"""
    @plugin.hook_add_command("bot")
    def bot_command(self, params=None, **kwargs):
    	self.irc.reply("Testing")

