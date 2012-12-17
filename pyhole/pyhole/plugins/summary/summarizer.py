
import hashlib
import re
from menu import *

def hash(string):
  return hashlib.md5(string).hexdigest()

class GroupedSummarizer:
  def __init__(self):
    self.groups = {}
    self.count = 0

  def add(self, id, message):
    item = Result(id, message)
    if item.hash not in self.groups:
      self.groups[item.hash] = ResultSet(message)
    self.groups[item.hash].add(item)
    self.count += 1

  def menu(self):
    return Menu(InteractiveList(self.groups.values()))

class NumericalSummarizer:
  def __init__(self, match_string):
    subs = {
      "s": "\S+",
      "n": "[0-9.]+"
    }
    self.hosts = []
    self.matches = []
    self.combiners = []
    matches = re.findall("(<([A-Za-z0-9._\\+:-]+)>|\s+)", match_string)
    match_string = ""
    i = 1
    for match in matches:
      combiner = match[1]
      if len(combiner) > 0:
        # We're dealing with a <combiner>
        args = combiner.split(":")
        while len(args) < 3: args.append("") 
        self.combiners.append(self.find_combiner(args[0], args[1], args[2]))
        self.matches.append([])
        match_string += "(" + subs[args[0]] + ")"
      else:
        match_string += "\s+"

    self.match_string = match_string

  def find_combiner(self, type, combiner, name):
    if combiner == "concat":
      return ConcatCombiner(name, type)
    elif combiner == "avg":
      return AverageCombiner(name, type)
    elif combiner == "sum":
      return SumCombiner(name, type)
    elif combiner == "product":
      return ProductCombiner(name, type)
    elif combiner == "max":
      return MaxCombiner(name, type)
    elif combiner == "min":
      return MinCombiner(name, type)
    elif combiner == "unique":
      return UniqueCombiner(name, type)
    return NullCombiner(name, type)

  def add(self, id, message):
    matches = re.search(self.match_string, message)
    results = matches.groups()
    self.hosts.append(id)
    for i in range(len(results)):
      self.combiners[i].add(id, results[i])

  def menu(self):
    items = []
    for i in range(len(self.combiners)):
      if isinstance(self.combiners[i], NullCombiner): continue
      # items.append("Variable %d (%s) - %s" % (i+1, self.combiners[i].type, self.combiners[i].summary()))
      items.append("%s (%s) - %s" % (self.combiners[i].name, self.combiners[i].type, self.combiners[i].summary()))

    interactive_list = InteractiveList(items)
    interactive_list.show_numbers = False
    interactive_list.show_pages = False
    interactive_list.perpage = len(self.combiners)
    return Menu(Prepender(
        "%d total entries" % len(self.hosts),
        interactive_list))

class Combiner:
  def __init__(self, name, type):
    if len(name) == 0:
      name = "var"
    self.name = name
    self.type = type
  def add(self, id, item):
    pass
  def summary(self):
    return ""

class NullCombiner(Combiner):
  def summary(self):
    return "String"

class ProductCombiner(Combiner):
  def __init__(self, name, type):
    Combiner.__init__(self, name, type)
    self.total = float(1)
  def add(self, id, item):
    self.total *= float(item)
  def summary(self):
    return str(self.total)

class AverageCombiner(Combiner):
  def __init__(self, name, type):
    Combiner.__init__(self, name, type)
    self.total = float(0)
    self.count = 0
  def add(self, id, item):
    self.total += float(item)
    self.count += 1
  def summary(self):
    if self.count == 0:
      return "No items"
    return str(self.total / self.count)

class SumCombiner(Combiner):
  def __init__(self, name, type):
    Combiner.__init__(self, name, type)
    self.total = float(0)
  def add(self, id, item):
    self.total += float(item)
  def summary(self):
    return str(self.total)

class MinCombiner(Combiner):
  def __init__(self, name, type):
    Combiner.__init__(self, name, type)
    self.min = None
    self.min_items = []
  def add(self, id, item):
    item = float(item)
    if self.min == None:
      self.min = item
      self.min_items = [id]
    elif item <= self.min:
      if item < self.min:
        self.min_items = []
      self.min_items.append(id)
      self.min = item
  def summary(self):
    return "*" + ", ".join(self.min_items) + "*: " + str(self.min)

class MaxCombiner(Combiner):
  def __init__(self, name, type):
    Combiner.__init__(self, name, type)
    self.max = None
    self.max_items = []
  def add(self, id, item):
    item = float(item)
    if self.max == None:
      self.max = item
      self.max_items = [id]
    elif item >= self.max:
      if item > self.max:
        self.max_items = []
      self.max_items.append(id)
      self.max = item
  def summary(self):
    return "*" + ", ".join(self.max_combiner) + "*: " + str(self.max)

class ConcatCombiner(Combiner):
  def __init__(self, name, type):
    Combiner.__init__(self, name, type)
    self.all = []
  def add(self, id, item):
    self.all.append(str(item))
  def summary(self):
    return " || ".join(self.all)

class UniqueCombiner(Combiner):
  def __init__(self, name, type):
    Combiner.__init__(self, name, type)
    self.all = []
  def add(self, id, item):
    item = str(item)
    if item not in self.all:
      self.all.append(item)
  def summary(self):
    return " || ".join(self.all)

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
    servers_len = len(self.items)
    summary = "*"
    for key in range(min(servers_len, self.MAX_SERVERS_SUMMARY)):
      summary += self.items[key].id + ", "
    summary = summary[0:-2]
    if servers_len > self.MAX_SERVERS_SUMMARY:
      summary += " (and %d more..)" % (servers_len - self.MAX_SERVERS_SUMMARY)
    summary += "*\n"
    if len(self.message) > self.MAX_SUMMARY_LENGTH:
      summary += "%s...\n" % self.message[0:self.MAX_SUMMARY_LENGTH]
    else:
      summary += "%s\n" % self.message
    return summary

  def display(self):
    summary = "====== Full Output =====\n"
    summary += "%s\n\n" % (self.message)
    summary += "====== Servers =====\n"
    for result in self.items:
      summary += " * %s\n" % (result.id)
    summary += "\n"
    return summary




