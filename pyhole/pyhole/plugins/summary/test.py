import sys
from summarizer import *
from menu import *
import random

summarizer = NumericalSummarizer("<n:dist>, <s:sort>")

for i in range(71):
	summarizer.add("test", "%d, vt%d" % (random.randint(0, 100), random.randint(0, 1000)))

menu = summarizer.menu()
print menu.display()

