from concurrent.futures import ThreadPoolExecutor
import time

import Recoder
import Classification

def Main():
  print("開始")
  with ThreadPoolExecutor() as executor:
    executor.submit(Recoder.Start)
    executor.submit(Classification.Start)
  print("終了")

if __name__ == "__main__":
  Main()
