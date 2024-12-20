import os
import time
import psutil

dir = f"output/ResourceLog/"
os.makedirs(dir, exist_ok=True)

for i in range(10000):
  path = f"{dir}resource-{i}.csv"
  if not os.path.exists(path):
    break

with open(path, "a") as f:
  f.write(f"unix_time,cpu_percent,mem_percent\n")

while True:
  unix_time = time.time()
  cpu_percent = psutil.cpu_percent(percpu=False)
  mem_percent = psutil.virtual_memory().percent

  mes = f"{unix_time},{cpu_percent},{mem_percent}\n"
  mesP = f"unix time: {unix_time}s, CPU: {cpu_percent}%, Memory: {mem_percent}%"

  with open(path, "a") as f:
    f.write(mes)

  print(mesP)

  time.sleep(1)
