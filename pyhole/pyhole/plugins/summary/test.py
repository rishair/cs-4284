
from summarizer import *
from menu import *

summarizer = NumericalSummarizer("avg%s name%avg%n")

summarizer.add("test", "testing 32")
summarizer.add("test", "monkey 24")
summarizer.add("test", "hello 44")

menu = summarizer.menu()
print menu.display()
