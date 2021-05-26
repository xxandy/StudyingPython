import sys

# -----------------------------
class CacheEntry:
  #CacheEntry class constructor
  def __init__(self, nUrl, nContents):
    self.url = nUrl
    self.contents = nContents
    self.next = None
    self.prev = None

  #CacheEntry method: replace contents
  def setContents(self, newContents):
    self.contents = newContents



# -----------------------------
class RecentCache:
  MAX_ENTRIES = 10

  # RecentCache class constructure
  def __init__(self):
    self.entryDict = {} #   { 'url1': CacheEntry, 'url2', CacheEntry2 ...}
    self.listHead = None
    self.listTail = None
    self.nEntries = 0

  # RecentCache method: refresh url1
  def refreshURL( self, url, contents):
    # Locals: searchR, newEntry, tmpLink

    searchR = self.entryDict.get( url )

    # If the key is found
    if searchR:
      searchR.setContents( contents )
      # if this is the last element, we are done
      if not ( searchR is self.listTail ):
        if searchR.prev:
          #not the first element.  skip it here (unlink)
          # also, we know the list has at least 3 elements
          #  (as searchR is not head and not tail).
          searchR.prev.next = searchR.next
        else:
          self.listHead = searchR.next

        # we know there is a next because this is not the end of the list
        searchR.next.prev = searchR.prev

        searchR.next = None
        self.listTail.next = searchR
        searchR.prev = self.listTail
        self.listTail = searchR

    #key not found, must add it
    else:
      newEntry = CacheEntry ( url, contents )

      if self.listTail:
        self.listTail.next = newEntry
        newEntry.prev = self.listTail
      self.listTail = newEntry

      if not self.listHead:
        self.listHead = newEntry

      self.entryDict[ url ] = newEntry # make it easy to search

      if self.nEntries < self.MAX_ENTRIES:
        self.nEntries = self.nEntries + 1
      else:
        self.entryDict.pop( self.listHead.url )
        tmpLink = self.listHead
        self.listHead = self.listHead.next
        self.listHead.prev = None # this is not the head, so it has no prev
        tmpLink.prev = None # remove references from it, let it die
        tmpLink.next = None
  # End of refreshURL

  # RecentCache method: print all objects, and also tests whether
  #    the doubly-linked list is oredered correctly, both forwards and
  #    backwards
  def printAll(self):
    comparestack = []
    iterator = self.listHead
    ix = 0
    print("--Iterate Forwards, print and stack:")
    while iterator:
      print( ix, 'url: ', iterator.url, '  contents: ', iterator.contents )
      comparestack.append( iterator )
      iterator = iterator.next
      ix = ix + 1

    iterator = self.listTail
    ix = ix - 1
    # --Iterate Backwards, comparing
    while iterator:
      if not (comparestack.pop() is iterator):
        print("ERROR: UNMATCHED VALUE!!!")
      iterator = iterator.prev
      ix = ix - 1



###################################
#### Main ########
def say_hello_to(name):
  print("========== START =========")

  print("TEST1:  Basic fill")
  rc = RecentCache()
  rc.refreshURL( 'google', 'awesome')
  rc.refreshURL( 'yahoo', 'ok')
  rc.refreshURL( 'bing', 'lackluster')

  rc.printAll()
  print("--")

  print("TEST2:  Update Middle")
  rc.refreshURL( 'yahoo', 'shabby')
  rc.printAll()
  print("--")

  print("TEST3:  Update First")
  rc.refreshURL( 'google', 'ultra')
  rc.printAll()
  print("--")


  print("TEST4:  Update Last")
  rc.refreshURL( 'google', 'gorgonzola')
  rc.printAll()
  print("--")


  print("TEST5: Fill up")
  rc.refreshURL( 'a04', 'awesome')
  rc.refreshURL( 'a05', 'ok')
  rc.refreshURL( 'a06', 'lackluster')
  rc.refreshURL( 'a07', 'awesome')
  rc.refreshURL( 'a08', 'ok')
  rc.refreshURL( 'a09', 'lackluster')
  rc.refreshURL( 'a10', 'awesome')
  rc.printAll()
  print("--")


  print("TEST6: Overflow")
  rc.refreshURL( 'overflow', 'finish!')
  rc.printAll()
  print("--")


  print("TEST7: Refesh middle after overflow")
  rc.refreshURL( 'google', 'gorgonzola')
  rc.printAll()
  print("--")

  print("TEST8: Refesh last after overflow")
  rc.refreshURL( 'google', 'cheddar')
  rc.printAll()
  print("--")

  print("TEST9: Refesh first after overflow")
  rc.refreshURL( 'yahoo', 'shabby')
  rc.printAll()
  print("--")



  print("========== END =========")

  print("Hello %s!" % name)
