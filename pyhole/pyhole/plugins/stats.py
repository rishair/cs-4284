"""Stats Plugin"""

import commands
import socket

from pyhole import irc
from pyhole import plugin
from pyhole import utils


class Stats(plugin.Plugin):
    """Prints hostname and IP"""

    @plugin.hook_add_command("stats")
    def stats(self, params=None, **kwargs):
        """Return hostname and ip address of machine bot is running on."""
        hostname = socket.gethostname()
        ipv4 = ''
        
        s = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error, msg:
            s = None
        try:
            # Google's public DNS server
            s.connect(("8.8.8.8", 53))
        except socket.error, msg:
            s.close()
            s = None
        if (s is None):
            ipv4 = "Unable to retrieve IPv4 address."
        else:
            ipv4 = s.getsockname()[0]
            s.close()

        self.irc.reply("Hostname: %s" % hostname)
        self.irc.reply("IPv4: %s" % ipv4)

