import time
import pandas as pd
import traceback

import RawData
import ProcessCtrl
import FlowPic
import UI.RichTable as RichTable
import Eval
import RouteRule
import UpdateRoute
import TimeLogger

def Start():
  try:
    # ルータの設定
    router1 = UpdateRoute.Router("192.168.10.11")
    router2 = UpdateRoute.Router("192.168.10.14")

    # 固定経路を追加
    router1.SetStaticRoute({
      "0.0.0.0/0": "192.168.9.2"
    })
    router2.SetStaticRoute({
      "0.0.0.0/0": "192.168.10.1",
      "192.168.9.0/24": "192.168.8.2",
      "192.168.11.0/24": "192.168.8.2"
    })

    while True:
      # 時刻ロガー
      timeLogger = TimeLogger.TimeLogger()
      timeLogger.Logger("データ読み込み開始")
      
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
      RouteTable = {}
      sourceRouteTable = {}
      tt = RichTable.TrafficMini()
      for idx, row in targetList.iterrows():
        timeLogger.Logger("フロー情報処理開始")
        
        #df1 = df[(df["SrcIP"] == row["SrcIP"]) & (df["DstIP"] == row["DstIP"]) & (df["SrcPort"] == row["SrcPort"]) & (df["DstPort"] == row["DstPort"])]
        df1 = df[(df["SrcIP"] == row["SrcIP"]) & (df["DstIP"] == row["DstIP"])]
        # 統計の計算
        length = df1["Length"].sum()
        startTime = df1["Timestamp"].min()
        endTime = df1["Timestamp"].max()
        duration = endTime - startTime

        # 0.1MB以上かつ1分以上の通信のみ処理の対象とする
        if length < 100000 or duration < 60:
          #print(f"Skip: {row["SrcIP"]}-{row["DstIP"]}, {length}B")
          timeLogger.Clear()
          continue

        # 画像化
        timeLogger.Logger("フロー画像生成開始")
        FlowPic.Generate(df1, "output/tmp.png")

        # 評価
        timeLogger.Logger("CNN評価開始")
        predict = Eval.Eval("output/tmp.png")
        timeLogger.Logger("CNN評価終了")

        # 表示
        tt.add(idx, row["SrcIP"], row["DstIP"], length, duration, predict["predicted"], predict["probabilities"])

        # 低精度
        if predict["probabilities"] < 0.6:
          timeLogger.Clear()
          continue
        
        timeLogger.Logger("ルーティング制御開始")
        # ルールで分類
        if RouteRule.getRouteByLabel(predict["predicted"]):
          # ルーティング
          src = f"{row["SrcIP"]}/32"
          gw = "192.168.9.3"
          RouteTable[src] = gw
          # ソースルーティング
          src = f"{row["SrcIP"]}/32"
          dst = f"{row["DstIP"]}/32"
          sourceRouteTable.setdefault(src, []).append(dst)
        timeLogger.Logger("ルーティング制御終了")

        # 時刻ロガーの出力
        timeLogger.SetStreamId(idx)
        timeLogger.Write()

        # ファイル出力
        #df1.to_csv(f"output/{idx}.csv")

      # ルーティングテーブルの更新
      print(RouteTable)
      router1.UpdateRoute(RouteTable, {})
      router2.UpdateRoute({}, sourceRouteTable)

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
