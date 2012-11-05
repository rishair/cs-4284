"""Summary Test Plugin"""

import commands
import socket
import random

from pyhole import irc
from pyhole import plugin
from pyhole import utils



class SummaryTest(plugin.Plugin):
    """Tests the client-side summary"""

    @plugin.hook_add_command("sum")
    def summaryTest(self, params=None, **kwargs):
        """Test out the client-side summary using non-local sending"""
        
        # Simulate actual data to aggregate, send to the #reply channel
        self.irc.privmsg("#reply", "(sum, %s): This is test data: %s" % (hash(kwargs["full_message"]), random.randint(0,4)))

