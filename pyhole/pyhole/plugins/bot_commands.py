"""Summary Test Plugin"""

import commands
import socket
import random
import os

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
      self.irc.reply("Rank: %d, Random: %d" % (self.irc.rank, random.randint(0, 100)))

  @plugin.hook_add_command("loadavg")
  def loadavg(self, params=None, **kwargs):
    self.irc.reply("%f %f %f" % os.getloadavg())

  @plugin.hook_add_command("done")
  def thanks(self, params=None, **kwargs):
    print self.irc.rank
    if self.irc.rank >= 0:
      words = "Thanks for listening :)".split(" ")
      word = words[self.irc.rank % len(words)]
      self.irc.reply(word)