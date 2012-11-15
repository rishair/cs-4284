"""Summary Test Plugin"""

import commands
import socket
import random

from pyhole import irc
from pyhole import plugin
from pyhole import utils
from pyhole.plugins.summary import summarizer

class UserManager:
	def __init__(self):
		self._users = {}

	def setup_user(self, nick):
		if nick not in self._users:
			self._users[nick] = [None, []]

	def add_user_hash(self, nick, h):
		self.setup_user(nick)
		self._users[nick][0] = h
		self._users[nick][1].append(h)

	def user_hash(self, nick):
		self.setup_user(nick)
		return self._users[nick][0]

	def user_hashes(self, nick):
		self.setup_user(nick)
		return self._users[nick][1]


class Summarizer(plugin.Plugin):
	"""Tests the server-side summary"""
	def __init__(self, irc):
		self._summarizers = {}
		self._users = UserManager()
		plugin.Plugin.__init__(self, irc)

	def summarizer(self, hash):
		if hash not in self._summarizers:
			self._summarizers[hash] = summarizer.Summarizer()
		return self._summarizers[hash]

	def summarizers(self):
		return self._summarizers.keys()

	@plugin.hook_add_msg_regex(".")
	def bot_command(self, params=None, **kwargs):
		channel = self.irc.target
		nick = self.irc.source
		message = kwargs["full_message"]
		private = kwargs["private"]

		if private:
			if message[0] == "#":
				channel = "#" + message.split(" ", 1)[0].strip("#")
				message = message.split(" ", 1)[1]
			else:
				auto_channel = None
				for c in self.irc.channels:
					if auto_channel is None: auto_channel = c.strip("#")
					if c.strip("#") != auto_channel:
						auto_channel = None
						break
				if auto_channel != None: channel = "#" + auto_channel

		if channel[0:3] == "###":
			split = message.split(";", 1)
			if len(split) > 1:
				# Message from a bot
				hash = split[0]
				message = split[1]
				self.summarizer(hash).add(nick, message)
			else:
				pass
		else:
			sums = self.summarizers()

			if message == "jobs":
				self.irc.normal_reply(", ".join(self._users.user_hashes(nick)))
			elif message[0] == ".":
				md5 = self.irc.generate_hash(nick, message)
				self._users.add_user_hash(nick, md5)
				self.irc.normal_reply("Processing job %s" % md5)
				self.irc.send_to_bots(channel, md5, message)
			else:
				md5 = self._users.user_hash(nick)
				self.irc.normal_reply("Showing job %s" % md5)
				menu = self.summarizer(md5).menu()
				menu.query(message)
				self.irc.normal_reply(menu.display())