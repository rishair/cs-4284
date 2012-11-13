
"""Version plugin"""

from pyhole import plugin

class Version(plugin.Plugin):
    """Used to test how many plugins actually update with an update command"""

    @plugin.hook_add_command("v")
    def update(self, params=None, **kwargs):
        """Spit out version"""
        
        # Simulate actual data to aggregate, send to the reply channel
        self.irc.reply("v;%s;1" % (hash(kwargs["full_message"] + self.irc.source)))