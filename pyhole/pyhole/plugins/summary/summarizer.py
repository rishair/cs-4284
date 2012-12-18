
from menu import *
import exceptions
import hashlib
import math
import re

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
      "n": "[0-9.-]+"
    }
    self.hosts = []
    self.matches = []
    self.combiners = []
    matches = re.findall("(<([A-Za-z0-9._\\+:-]+)>|\s+|[^<]+)", match_string)
    match_string = ""
    i = 1
    for match in matches:
      combiner = match[1]
      if len(combiner) > 0:
        # We're dealing with a <combiner>
        args = combiner.split(":")
        while len(args) < 2: args.append("")
        first = self.find_combiner(args[0], args[1])
        first = None
        last = None
        for i in range(1, len(args)):
          item = self.find_combiner(args[0], args[i])
          if first == None:
            first = item
            last = item
          else:
            last.output = item
            last = item
        self.combiners.append(first)
        self.matches.append([])
        match_string += "(" + subs[args[0]] + ")"
      else:
        if re.match("\s+", match[0]):
          match_string += "\s+"
        else:
          match_string += re.escape(match[0])
    self.match_string = match_string

  def find_combiner(self, type, combiner):
    combiner_parts = combiner.split(",")
    combiner_name = combiner_parts[0]
    combiner_params = combiner_parts[1:]

    combiners = {
      "average":      AverageCombiner,
      "avg":          AverageCombiner,
      "concat":       ConcatCombiner,
      "dist":         DistributionCombiner,
      "distribution": DistributionCombiner,
      "max":          MaxCombiner,
      "maximum":      MaxCombiner,
      "min":          MinCombiner,
      "minimum":      MinCombiner,
      "sort":         SortCombiner,
      "sum":          SumCombiner,
      "unique":       UniqueCombiner,
    }
    if combiner_name in combiners:
      return combiners[combiner_name](type, combiner_params)
    return NullCombiner(type, combiner_params)

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
      self.combiners[i].propogate_output()
      # items.append("Variable %d (%s) - %s" % (i+1, self.combiners[i].type, self.combiners[i].summary()))
      items.append("%s (%s): %s" % ("var " + str(i), self.combiners[i].type, self.combiners[i].final_summary()))

    interactive_list = InteractiveList(items)
    interactive_list.show_numbers = False
    interactive_list.show_pages = False
    interactive_list.perpage = len(self.combiners)
    return Menu(Prepender(
        "%d total entries" % len(self.hosts),
        interactive_list))

class Combiner:
  def __init__(self, type, params):
    self.type = type
    self.output = None
    self.params = params
  def add(self, id, item):
    pass
  def join(self, items, joiner = " | "):
    return joiner.join(map(str, items))
  def summary(self):
    return ""
  def output_error(self):
    if not isinstance(self.output, Combiner):
      return "%s is not a valid combiner" % self.output.__class__.__name__ 
    if not isinstance(self, ProducerCombiner):
      return "%s is not a valid output combiner" % self.__class__.__name__
  def propogate_output(self):
    error = self.output_error()
    if self.output == None or error != None:
      return False
    out = self.out()
    for item in out:
      self.output.add("id", item)
    return True
  def final_summary(self):
    error = self.output_error()
    if self.output != None:
      if error == None:
        return self.output.final_summary()
      else:
        return error
    return self.summary()

class ProducerCombiner(Combiner):
  def out(self):
    return []

class NullCombiner(ProducerCombiner):
  def summary(self):
    return "String"

class ProductCombiner(ProducerCombiner):
  def __init__(self, type, params):
    Combiner.__init__(self, type, params)
    self.total = float(1)
  def add(self, id, item):
    self.total *= float(item)
  def summary(self):
    return str(self.total)
  def out(self):
    return self.total

class AverageCombiner(ProducerCombiner):
  def __init__(self, type, params):
    Combiner.__init__(self, type, params)
    self.total = float(0)
    self.count = 0
  def add(self, id, item):
    self.total += float(item)
    self.count += 1
  def summary(self):
    if self.count == 0:
      return "No items"
    return str(self.total / self.count)
  def out(self):
    if self.count == 0: return 0
    return self.total / self.count

class SumCombiner(ProducerCombiner):
  def __init__(self, type, params):
    Combiner.__init__(self, type, params)
    self.total = float(0)
  def add(self, id, item):
    self.total += float(item)
  def summary(self):
    return str(self.total)
  def out(self):
    return self.total

class MinCombiner(ProducerCombiner):
  def __init__(self, type, params):
    Combiner.__init__(self, type, params)
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
    return str(self.min) + " (" + ", ".join(self.min_items) + ")"
  def out(self):
    return self.min

class MaxCombiner(ProducerCombiner):
  def __init__(self, type, params):
    Combiner.__init__(self, type, params)
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
    return  str(self.max) + " (" + ", ".join(self.max_items) + ")"
  def out(self):
    return self.max

class ConcatCombiner(ProducerCombiner):
  def __init__(self, type, params):
    Combiner.__init__(self, type, params)
    self.all = []
  def add(self, id, item):
    self.all.append(str(item))
  def summary(self):
    return self.join(self.all)
  def out(self):
    return self.all

class CountCombiner(ProducerCombiner):
  def __init__(self, type, params):
    Combiner.__init__(self, type, params)
    self.count = 0
  def add(self, id, item):
    self.count += 1
  def summary(self):
    return str(self.count)
  def out(self):
    return self.count

class UniqueCombiner(ProducerCombiner):
  def __init__(self, type, params):
    Combiner.__init__(self, type, params)
    self.all = []
  def add(self, id, item):
    item = str(item)
    if item not in self.all:
      self.all.append(item)
  def summary(self):
    return self.join(self.all)
  def out(self):
    return self.all

class SortCombiner(Combiner):
  def __init__(self, type, params):
    Combiner.__init__(self, type, params)
    self.all = []
  def add(self, id, item):
    try:
      item = float(item)
    except exceptions.ValueError:
      pass
    for i in range(len(self.all)):
      if item < self.all[i]:
        self.all.insert(i, item)
        return
    self.all.append(item)
  def summary(self):
    return self.join(self.all)
  def out(self):
    return self.all


class DistributionCombiner(Combiner):
  def __init__(self, type, params):
    Combiner.__init__(self, type, params)
    self.all = []
    self.total = 0
    self.sqtotal = 0

  def add(self, id, item):
    item = float(item)
    self.total += item
    self.sqtotal += item*item
    for i in range(len(self.all)):
      if item < self.all[i]:
        self.all.insert(i, item)
        return
    self.all.append(item)

  def percentile(self, percent):
    index = percent * len(self.all)
    if percent == 1:
      index -= 1
    if int(index) == index:
      return self.all[int(index)]
    else:
      prev = float(self.all[int(index)])
      next = float(self.all[min(len(self.all) - 1, int(index) + 1)])
      return (prev + next) / 2 + (next - prev) * (index % 1)

  def slice(self, percent):
    return self.all[0] + (self.all[-1] - self.all[0]) * percent

  def find_slice(self, val):
    return (val - self.all[-1]) / (self.all[0] - self.all[-1])

  def google_link(self):
    ranges = []
    steps = 10
    increment = (self.all[-1] - self.all[0]) / float(steps)
    if increment == 0: return "Unavailable"
    d = str(max(0, int(math.floor(abs(math.log(abs(increment), steps))))))
    for i in range(0, steps):
      sliced = self.slice(i / float(steps))
      ranges.append([("%." + d + "f-%." + d + "f") % (sliced, sliced + increment), 0])
    for item in self.all:
      sliced = self.find_slice(item)
      index = int(sliced * steps)
      if sliced == 1:
        index -= 1
      ranges[index][1] += 1

    url = "http://chart.apis.google.com/chart?cht=bvg&chs=600x300&chxt=x,y&chbh=a,0,1&chco=4D89F9&chds=a&"
    url += "chd=t:" + ",".join(map(lambda x: str(x[1]), ranges)) + "&"
    url += "chxl=0:|" + "|".join(map(lambda x: x[0], ranges)) + "&"
    url += "chtt=Distribution+of+%d+entries" % len(self.all)
    return url

  def summary(self):
    percentiles = [
      ("# of Items",             len(self.all)),
      (" > Highest",          self.percentile(1)),
      (" > 90th percentile",  self.percentile(.9)),
      (" > 75th percentile",  self.percentile(.75)),
      (" > 50th percentile",  self.percentile(.50)),
      (" > 25th percentile",  self.percentile(.25)),
      (" > 10th percentile",  self.percentile(.1)),
      (" > Lowest",           self.percentile(0)),
      (" > Mean",             self.total / len(self.all)),
      (" > Variance",         self.sqtotal / len(self.all)),
      (" > Std Deviation",    math.sqrt(self.sqtotal / len(self.all))),
      (" > Histogram",        self.google_link()),
    ]
    string = ""
    for item in percentiles:
      string += item[0] + ": " + str(item[1]) + "\n"
    return string


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

