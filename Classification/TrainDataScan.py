from concurrent.futures import ThreadPoolExecutor

from ..PacketFlowScan import Scan
import Classification

def Main():
  print("開始")
  Scan.TrainStart(1000)
  Classification.TrainStart()
  print("正常終了")

if __name__ == "__main__":
  Main()
