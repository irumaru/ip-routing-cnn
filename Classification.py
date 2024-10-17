import time
import pandas as pd
import traceback

import Recoder
import FlowPic

def Start():
  try:
    while True:
      # Dataframeへ変換
      with Recoder.rtLock:
        df = pd.DataFrame(Recoder.rt, columns=["SrcIP", "DstIP", "SrcPort", "DstPort", "Protocol", "Length", "Timestamp"])

      # リストの取得
      targetList = df.loc[:, ["SrcIP", "DstIP"]].drop_duplicates()

      #print(targetList)

      # サイズ統計
      for idx, row in targetList.iterrows():
        df1 = df[(df["SrcIP"] == row["SrcIP"]) & (df["DstIP"] == row["DstIP"])]
        length = df1["Length"].sum()

        # 10MB以上の通信
        # if length < 10000000:
        #   continue
        print(length)

        # 画像化
        FlowPic.generate(df1, f"{row['SrcIP']}-{row['DstIP']}")

      time.sleep(2)
  except:
    traceback.print_exc()
