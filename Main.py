from concurrent.futures import ThreadPoolExecutor
import time

import ProcessCtrl
import Recoder
import Classification

def Main():
  try:
    print("開始")
    with ThreadPoolExecutor() as executor:
      pr = executor.submit(Recoder.Start)
      pc = executor.submit(Classification.Start)
    print("異常終了")
  except KeyboardInterrupt:
    print("終了中")
    ProcessCtrl.Runnables.getInstance().setRunnable(False)
    while pr.running():
      print("Recoder: 終了待機")
      time.sleep(1)
    while pc.running():
      print("Classification: 終了待機")
      time.sleep(1)
    print("正常終了")

if __name__ == "__main__":
  Main()
