
import hashlib
import re
from menu import *

def hash(string):
  return hashlib.md5(string).hexdigest()

class Summarizer:
  def __init__(self):
    self.groups = {}
    self._menu = None
    self.count = 0

  def add(self, id, message):
    item = Result(id, message)
    if item.hash not in self.groups:
      self.groups[item.hash] = ResultSet(message)
    self.groups[item.hash].add(item)
    self.count += 1

  def menu(self):
    if self._menu is None:
      self._menu = Menu(InteractiveList(self.groups.values()))
    return self._menu


class Result:
  def __init__(self, id, message):
    self.id = id
    self.message = message
    self.hash = hash(message)

  def __str__(self):
    return bcolors.OKBLUE + self.id + ": " + bcolors.ENDC + self.message

class ResultSet (InteractiveItem):
  MAX_SUMMARY_LENGTH = 50
  MAX_SERVERS_SUMMARY = 5

  def __init__(self, message = ""):
    self.items = []
    self.message = message

  def add(self, result):
    self.items.append(result)

  def find(self, query):
    high = 0
    for e in self.items:
      if e.id == query:
        high = max(high, 3)
      elif query in e.id:
        high = max(high, 2)
    if query in self.message:
      return 1
    return high

  def display_short(self):
    summary = ""
    space = " " * len(summary)
    # Add the "Message" line
    summary += "Message: "
    if len(self.message) > self.MAX_SUMMARY_LENGTH:
      summary += "%s...\n" % self.message[0:self.MAX_SUMMARY_LENGTH]
    else:
      summary += "%s\n" % self.message 
    # Add the "Servers" line
    summary += "%sServers: " % space
    servers_len = len(self.items)
    for key in range(min(servers_len, self.MAX_SERVERS_SUMMARY)):
      summary += self.items[key].id + ", "
    summary = summary[0:-2]
    if servers_len > self.MAX_SERVERS_SUMMARY:
      summary += " (and %d more..)" % (servers_len - self.MAX_SERVERS_SUMMARY)
    summary += "\n"
    return summary

  def display(self):
    summary = "====== Full Output =====\n"
    summary += "%s\n\n" % (self.message)
    summary += "====== Servers =====\n"
    for result in self.items:
      summary += " * %s\n" % (result.id)
    summary += "\n"
    return summary




