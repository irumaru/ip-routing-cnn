import time
import pandas as pd
import traceback

import RawData
import ProcessCtrl
import FlowPic
import UI.RichTable as RichTable
import Eval

def Start():
  try:
    while True:
      # Dataframeへ変換
      rt = RawData.Table.getInstance().getRawTable()
      rtLock = RawData.Table.getInstance().getRawTableLock()
      with rtLock:
        df = pd.DataFrame(rt, columns=["SrcIP", "DstIP", "SrcPort", "DstPort", "Protocol", "Length", "Timestamp"])
      #df = pd.DataFrame(rt, columns=["SrcIP", "DstIP", "SrcPort", "DstPort", "Protocol", "Length", "Timestamp"])

      # リストの取得
      # targetList = df.loc[:, ["SrcIP", "SrcPort", "DstIP", "DstPort"]].drop_duplicates()
      targetList = df.loc[:, ["SrcIP", "DstIP"]].drop_duplicates()

      #print(targetList)

      # サイズ統計
      tt = RichTable.Traffic()
      for idx, row in targetList.iterrows():
        #df1 = df[(df["SrcIP"] == row["SrcIP"]) & (df["DstIP"] == row["DstIP"]) & (df["SrcPort"] == row["SrcPort"]) & (df["DstPort"] == row["DstPort"])]
        df1 = df[(df["SrcIP"] == row["SrcIP"]) & (df["DstIP"] == row["DstIP"])]
        # 統計の計算
        length = df1["Length"].sum()
        startTime = df1["Timestamp"].min()
        endTime = df1["Timestamp"].max()
        duration = endTime - startTime

        # 1MB以上の通信
        if length < 1000000:
          continue

        # 画像化
        FlowPic.Generate(df1, "output/tmp.png")

        # 評価
        label = Eval.Eval("output/tmp.png")

        # 表示
        tt.add(idx, row["SrcIP"], "", row["DstIP"], "", "", length, duration, label)

        # ファイル出力
        #df1.to_csv(f"output/{idx}.csv")

      tt.print()

      time.sleep(2)

      # プロセス終了
      if ProcessCtrl.Runnables.getInstance().getRunnable() == False:
        return
  except:
    traceback.print_exc()



def TrainStart():
  try:
    # Dataframeへ変換
    rt = RawData.Table.getInstance().getRawTable()
    rtLock = RawData.Table.getInstance().getRawTableLock()
    with rtLock:
      df = pd.DataFrame(rt, columns=["SrcIP", "DstIP", "SrcPort", "DstPort", "Protocol", "Length", "Timestamp"])

    # リストの取得
    # targetList = df.loc[:, ["SrcIP", "SrcPort", "DstIP", "DstPort"]].drop_duplicates()
    targetList = df.loc[:, ["SrcIP", "DstIP"]].drop_duplicates()

    #print(targetList)

    # サイズ統計
    tt = RichTable.Traffic()
    for idx, row in targetList.iterrows():
      #df1 = df[(df["SrcIP"] == row["SrcIP"]) & (df["DstIP"] == row["DstIP"]) & (df["SrcPort"] == row["SrcPort"]) & (df["DstPort"] == row["DstPort"])]
      df1 = df[(df["SrcIP"] == row["SrcIP"]) & (df["DstIP"] == row["DstIP"])]
      # 統計の計算
      length = df1["Length"].sum()
      startTime = df1["Timestamp"].min()
      endTime = df1["Timestamp"].max()
      duration = endTime - startTime

      # 1MB以上の通信
      if length < 1000000:
        continue

      # 表示
      tt.add(idx, row["SrcIP"], "", row["DstIP"], "", "", length, duration)

      # 画像化
      FlowPic.Generate(df1, f"{idx}")

      # ファイル出力
      df1.to_csv(f"output/{idx}.csv")

    tt.print()

    # プロセス終了
    return
  except:
    traceback.print_exc()
