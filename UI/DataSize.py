import math

def Print(size):
  units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB")
  i = math.floor(math.log(size, 1024)) if size > 0 else 0
  size = round(size / 1024 ** i, 2)

  return f"{size} {units[i]}"
