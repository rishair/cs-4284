

class MenuResponse:
  def __init__(self):
    self.stack_item = None
    self.stack_seek = 0
    self.message = ""

class Menu:
  def __init__(self, item = None):
    self.stack = []
    self.notification = ""
    if item != None:
      self.push(item)

  def push(self, item):
    self.stack.append(item)

  def top(self):
    return self.stack[-1]

  def query(self, message):
    response = None
    if message == "back":
      response = MenuResponse()
      response.stack_seek = -1
    elif message in ["show", "display"]:
      return
    else:
      response = self.top().response(message)
    if response.stack_seek < 0:
      for i in range(min(-response.stack_seek, len(self.stack) - 1)):
        self.stack.pop()
    if response.stack_item:
      self.push(response.stack_item)
    if len(response.message) > 0:
      self.notification = response.message + "\n"

    return response.message

  def display(self):
    response = self.notification + self.top().display()
    self.notification = ""
    return response

class InteractiveItem:
  def response(self, message):
    return MenuResponse()
  def find(self, query):
    return False
  def display(self):
    pass
  def __str__(self):
    return self.display()

class Tester(InteractiveItem):
  def __init__(self, value):
    self.value = value
  def display(self):
    return "This is tester #%d, how are you?" % self.value

class RankedList:
  def __init__(self, unique=True):
    self.ranks = {}
    self.seen = {}
    self.unique = unique

  def add(self, rank, item):
    if item in self.seen:
      if rank > self.seen[item]:
        self.ranks[self.seen[item]].remove(item)
        self.seen[item] = rank
      else:
        return False

    if rank not in self.ranks:
      self.ranks[rank] = []
    self.ranks[rank].append(item)
    return True

  def list(self):
    keys = self.ranks.keys()
    keys.sort()
    merged = []
    for k in keys:
      merged.extend(self.ranks[k])
    return merged

class Prepender (InteractiveItem):
  def __init__(self, text, interactive):
    self.text = text
    self.interactive = interactive

  def display(self):
    return self.text + "\n" + self.interactive.display()

  def find(self, query):
    return self.interactive.find(query)

  def response(self, message):
    return self.interactive.response(message)

  def current_range(self):
    return self.interactive.current_range()

  def page_display(self):
    return self.interactive.page_display()

class InteractiveList (InteractiveItem):
  def __init__(self, l):
    self.list = l
    self.cursor = 0
    self.perpage = 3
    self.show_pages = True
    self.show_numbers = True

  def find(self, query):
    ranked = RankedList()
    for k in self.list:
      val = k.find(query)
      if val > 0:
        ranked.add(val, k)
    return InteractiveList(ranked.list())

  def response(self, message):
    response = MenuResponse()
    if message == "next":
      if self.cursor + self.perpage < len(self.list):
        self.cursor += self.perpage
    elif message == "prev":
      if self.cursor >= self.perpage:
        self.cursor -= self.perpage
    elif message.find("find ") == 0:
      query = message[5:]
      response.stack_item = self.find(query)
    else:
      try:
        response.stack_item = self.list[int(message) - 1]
      except:
        response.message = "Huh?"
    return response

  def current_range(self):
    return range(self.cursor, self.cursor + min(self.perpage, len(self.list) - self.cursor))

  def page_display(self):
    return "(%d of %d)\n\n" % (self.cursor + 1, len(self.list))
    # return "(page %d of %d)\n\n" % (self.cursor / self.perpage + 1, (len(self.list) - 1) / self.perpage + 1)

  def display(self):
    display = ""
    if self.show_pages:
      display += self.page_display()
    for i in self.current_range():
      item = self.list[i]
      if self.show_numbers:
        display += str(i + 1) + ". "
      if isinstance(item, InteractiveItem):
        display += item.display_short()
      else:
        display += item
      display += "\n"
    return display






