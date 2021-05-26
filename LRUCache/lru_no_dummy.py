#Super simple LRU  cache
# This version avoids a dummy entry

class Entry:
  def __init__(self, urlI, contentsI ):
    self.next_ = None
    self.contents_ = contentsI
    self.url_ = urlI

class Cache:
  def __init__(self, maxEntriesI ):
    self.maxEntries_ = maxEntriesI
    self.usedEntries_ = 0
    self.prevKey_ = {}
    # Entry records
    self.oldest_ = None
    self.newest_ = None

  def accessPage(self, url, contents):
    node = self.prevKey_.get(url)
    if node is not None:
      # unlink it from where it is
      if node is self:
        found = self.oldest_
        next = found.next_
        prev = self
        self.oldest_ = next
        if next is None:
          # removed the only element
          self.newest_ = None
          prev = self
          self.oldest_ = found
        else:
          self.prevKey_[ next.url_ ] = prev
          prev = self.newest_
          prev.next_ = found
      else:
        found = node.next_
        next = found.next_
        prev = node
        node.next_ = next
        if next is None:
          self.newest_ = prev
        else:
          self.prevKey_[ next.url_ ] = prev
        prev = self.newest_
        prev.next_ = found
      found.contents_ = contents
      found.next_ = None # its the last one now
      # ready to add this as if it was brand new
      node = found
    else:
      # make room if needed
      node = Entry( url, contents )
      if self.usedEntries_ >= self.maxEntries_:
        #unlink oldest element
        first = self.oldest_
        second = first.next_
        self.oldest_ = second
        self.prevKey_.pop( first.url_, None )
        self.prevKey_[second.url_] = self
        prev = self.newest_
        prev.next_ = node
      elif self.usedEntries_ == 0:
        self.usedEntries_ = 1
        self.oldest_ = node
        prev = self
      else:
        self.usedEntries_ += 1
        prev = self.newest_
        prev.next_ = node

    #now add new entry
    self.newest_ = node
    self.prevKey_[url] = prev

  def printContents(self):
    e = self.oldest_
    print("---list---")
    while e is not None:
      print( e.url_ + " " + e.contents_ )
      e = e.next_
    print("---map---")
    for item in self.prevKey_.items():
      print(item)
      
cache = Cache(4)

print()
print("-----test case 0")
cache.accessPage("a", "ACont")
cache.printContents()

print()
print("-----test case 1")
cache.accessPage("a", "AContV2")
cache.printContents()

print()
print("-----test case 2")
cache.accessPage("b", "BCont")
cache.accessPage("c", "CCont")
cache.accessPage("d", "DCont")
cache.printContents()


print()
print("-----test case 3")
cache.accessPage("e", "ECont")
cache.printContents()

print()
print("-----test case 4")
cache.accessPage("f", "FCont")
cache.printContents()

print()
print("-----test case 5")
cache.accessPage("d", "Dnewcontents")
cache.printContents()

print()
print("-----test case 6")
cache.accessPage("c", "Cnewcontents")
cache.printContents()


print()
print("-----test case 7")
cache.accessPage("c", "Creupdated")
cache.printContents()

print()
print("-----test case 8")
cache.accessPage("e", "Enewcontents")
cache.printContents()


print("--- done ---")
