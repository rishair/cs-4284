import sys
from summarizer import *
from menu import *
import random
import re
import exceptions


def expand_bots(message, bots):
  match = re.search("\[([ -~]+)\]", message)
  targets = None
  if match:
    all_targets = []
    targets = match.group(1).split(",")
    for i in range(len(targets)):
      target = targets[i].strip()
      try:
        target.index("*")
        target = "^" + re.escape(target).replace("\\*", ".*") + "$"
        for bot in bots:
          if re.match(target, bot):
            all_targets.append(bot)
      except exceptions.ValueError:
        all_targets.append(target)
  return re.sub("\[([ -~]+)\]", "[%s]" % ", ".join(all_targets), message)



print expand_bots("test [bot2, bot*]", ["bot5", "bot8", "botty"])



sys.exit(1)
summarizer = NumericalSummarizer("<n:dist>, <s:sort>")

for i in range(71):
  summarizer.add("test", "%f, vt%d" % (random.randint(0, 100) / 100.0, random.randint(0, 1000)))

menu = summarizer.menu()
print menu.display()

