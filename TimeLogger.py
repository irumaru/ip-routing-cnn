import os

class TimeLogger:
  def __init__(self):
    self.Clear()
  
  def Clear(self):
    self.log = []
  
  def Logger(self, label, time):
    self.log.append({"label": label, "time": time})
  
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
      f.write("label,time\n")
      for l in self.log:
        f.write(f"{l['label']},{l['time']}\n")
