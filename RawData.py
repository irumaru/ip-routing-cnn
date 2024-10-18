import threading
#import multiprocessing

import DataStruct.Raw as Raw

class Table:
  instance = None
  isInitialized = False

  def __init__(self):
    if not __class__.isInitialized:
      raise Exception("This class is a singleton!")
    else:
      __class__.isInitialized = True
    
    #self.manager = multiprocessing.Manager()
    self.RawTable = Raw.RawTable([])
    #self.RawTable = self.manager.list()
    self.RawTableLock = threading.Lock()
    #self.RawTableLock = self.manager.Lock()

  def getInstance():
    if __class__.instance == None:
      __class__.isInitialized = True
      __class__.instance = __class__()
    return __class__.instance
  
  def getRawTable(self):
    return self.RawTable
  
  def getRawTableLock(self):
    return self.RawTableLock
