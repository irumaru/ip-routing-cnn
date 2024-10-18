from concurrent.futures import ThreadPoolExecutor
import time

import ProcessCtrl
import Recoder
import Classification

def Main():
  print("開始")
  Recoder.TrainStart(1000)
  Classification.TrainStart()
  print("正常終了")

if __name__ == "__main__":
  Main()
