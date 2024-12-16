import traceback
import time

import RawData
import ProcessCtrl

def gc():
  try:
    while True:
      ss = time.time()

      rt = RawData.Table.getInstance().getRawTable()
      rtLock = RawData.Table.getInstance().getRawTableLock()
      removeCount = 0
      with rtLock:
        m = 0
        for row in rt:
          if(m < row["Timestamp"]):
            m = row["Timestamp"]
        for row in rt:
          if(row["Timestamp"] < m - 60):
            rt.remove(row)
            removeCount += 1
      
      se = time.time()

      print(f"GC Count:{removeCount}, time:{se - ss}")


      for i in range(10):
        # 待機
        time.sleep(1)
        # プロセス終了
        if ProcessCtrl.Runnables.getInstance().getRunnable() == False:
          return
  except:
    traceback.print_exc()

def Start():
  gc()
