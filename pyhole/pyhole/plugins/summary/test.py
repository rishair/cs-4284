import sys
from summarizer import *
from menu import *

summarizer = GroupedSummarizer()

summarizer.add("test", "Hostname: vt08, IPv4: 198.61.172.30")
summarizer.add("test", "Hostnamae: vt08, IPv4: 198.61.172.30")
summarizer.add("test", "Hostname: vt08, IPv4: 198.61.172.30")

menu = summarizer.menu()
print menu.display()

