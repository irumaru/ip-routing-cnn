import os
import time

class TimeLogger:
  def __init__(self):
    self.Clear()
  
  def Clear(self):
    self.log = []
  
  def Logger(self, label):
    unixTime = time.time()
    relativeTime = time.perf_counter()
    self.log.append({"label": label, "relativeTime": relativeTime, "unixTime": unixTime})
  
  def SetStreamId(self, streamId):
    self.streamId = streamId
  
  def Write(self):
    dir = f"output/timeLog/"
    os.makedirs(dir, exist_ok=True)

    for i in range(10000):
      path = f"{dir}{self.streamId}-{i}.csv"
      if not os.path.exists(path):
        break

    with open(path, "w") as f:
      f.write("label,relative time,unix time\n")
      for l in self.log:
        f.write(f"{l['label']},{l['relativeTime']},{l['unixTime']}\n")
