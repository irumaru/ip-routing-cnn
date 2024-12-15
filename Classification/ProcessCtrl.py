class Runnables:
  instance = None
  isInitialized = False

  def __init__(self):
    if not __class__.isInitialized:
      raise Exception("This class is a singleton!")
    else:
      __class__.isInitialized = True
    
    self.Runnable = True

  def getInstance():
    if __class__.instance == None:
      __class__.isInitialized = True
      __class__.instance = __class__()
    return __class__.instance
  
  def getRunnable(self):
    return self.Runnable
  
  def setRunnable(self, value):
    self.Runnable = value
