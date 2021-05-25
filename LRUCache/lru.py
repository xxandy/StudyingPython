#Super simple LRU  cache

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
    self.oldest_ = Entry(None, None) #wasted dummy
    self.newest_ = self.oldest_

  def accessPage(self, url, contents):
    node = self.prevKey_.get(url)
    if node is not None:
      # unlink it from where it is
      found = node.next_
      node.next_ = found.next_
    else:
      # make room if needed
      if self.usedEntries_ >= self.maxEntries_:
        #unlink oldest element
        first = self.oldest_.next_
        self.oldest_.next_  = first.next_
        self.prevKey_.pop( first.url_, None )
      else:
        self.usedEntries_ += 1
      node = Entry( url, contents )

    #now add new entry
    self.newest_.next_ = node
    self.newest_ = node
    self.prevKey_[url] = self.newest_

  def printContents(self):
    e = self.oldest_.next_
    print("---list---")
    while e is not None:
      print( e.url_ + " " + e.contents_ )
      e = e.next_
    print("---map---")
    for item in self.prevKey_.items():
      print(item)
      
cache = Cache(4)

cache.accessPage("a", "ACont")
cache.accessPage("b", "BCont")
cache.accessPage("c", "CCont")
cache.accessPage("d", "DCont")

cache.printContents()

cache.accessPage("e", "ECont")

cache.printContents()

cache.accessPage("f", "FCont")


cache.printContents()

print("--- done ---")
