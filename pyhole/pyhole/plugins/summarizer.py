"""Summary Test Plugin"""

import commands
import socket
import random
import re

from pyhole import irc
from pyhole import plugin
from pyhole import utils
from pyhole.plugins.summary import summarizer

class UserManager:
	def __init__(self):
		self._users = {}
		self._hashes = {}

	def setup_user(self, nick):
		if nick not in self._users:
			self._users[nick] = [None, []]

	def add_user_hash(self, nick, h):
		self.setup_user(nick)
		self._users[nick][0] = h
		self._hashes[h] = nick
		if h not in self._users[nick][1]:
			self._users[nick][1].append(h)

	def user_from_hash(self, hash):
		return self._hashes[hash]

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
		self._jobs = {}
		plugin.Plugin.__init__(self, irc)

	def summarizer(self, hash):
		if hash not in self._summarizers:
			if hash not in self._jobs:
				self._jobs[hash] = []
			job = self._jobs[hash]
			if len(job) <= 1:
				self._summarizers[hash] = summarizer.GroupedSummarizer()
			else:
				self._summarizers[hash] = summarizer.NumericalSummarizer(job[1].strip())
		return self._summarizers[hash]

	def summarizers(self):
		return self._summarizers.keys()

	def num_bots(self, channel):
		i = 0
		if channel in self.irc.names:
			for name in self.irc.names[channel]:
				if re.match("bot([0-9]+)*", name):
					i += 1
		return i

	@plugin.hook_add_msg_regex(".")
	def bot_command(self, params=None, **kwargs):
		channel = self.irc.target
		nick = self.irc.source.split("!")[0]
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

		broadcast_channel = "#" + channel.strip("#")

		if channel[0:2] == "##":
			split = message.split(";", 1)
			if len(split) > 1:
				# Message from a bot
				hash = split[0]
				message = split[1]
				summy = self.summarizer(hash)
				summy.add(nick, message)
				if self.num_bots(broadcast_channel) == summy.count:
					self.irc.target = self._users.user_from_hash(hash)
					self.irc.source = self.irc.target + "!" + self.irc.target
					self.bot_command(full_message="show", private=True)
			else:
				pass
		elif channel[0:1] == "#" and not private:
			self.irc.normal_reply("%s: If you PM me the same command I might be able to help you summarize the results." % nick)
		else:
			# Parse up the job and save it, including pipes, etc.
			sums = self.summarizers()

			if message == "jobs":
				self.irc.normal_reply(", ".join(self._users.user_hashes(nick)))
			elif message.startswith("setjob"):
				md5 = message.split(" ", 1)[1]
				self.irc.normal_reply("Job set to %s" % md5)
				self._users.add_user_hash(nick, md5)
			elif message[0] == ".":
				md5 = self.irc.generate_hash(nick, message)
				self._users.add_user_hash(nick, md5)
				self._jobs[md5] = message.split("|")
				self.irc.normal_reply("Processing job %s" % md5)
				self.irc.send_to_bots(channel, md5, message)
				self.irc.request_names([channel])
			else:
				md5 = self._users.user_hash(nick)
				self.irc.normal_reply("Showing job %s" % md5)
				menu = self.summarizer(md5).menu()
				menu.query(message)
				self.irc.normal_reply(menu.display())