import sys
from summarizer import *
from menu import *

summarizer = NumericalSummarizer("<s:concat> <n:avg:name>")

summarizer.add("test", "testing 32")
summarizer.add("test", "monkey 24")
summarizer.add("test", "hello 44")

menu = summarizer.menu()
print menu.display()

