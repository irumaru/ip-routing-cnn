import pandas as pd

import FlowPic

def Create(packetDataPath, trainDataDirPath, imageDuration):
  # データ読み込み
  df = pd.read_csv(packetDataPath)

  # 統計
  startTime = df["Timestamp"].min()
  endTime = df["Timestamp"].max()
  startTimeI = int(startTime)
  endTimeI = int(endTime)

  # print(startTime)
  # print(startTimeI)
  # print(endTime)
  # print(endTimeI)

  # データの切り出し&ループ
  # count = 0
  # for imageStartTime in range(startTimeI, endTimeI, imageDuration):
  #   df1 = df[(imageStartTime < df["Timestamp"]) & (df["Timestamp"] < imageStartTime + imageDuration)]
  #   Generate(workDir, df1, count)

  #   count += 1

  trainDataCount = 100
  slide = int((endTimeI - (startTimeI + imageDuration)) / trainDataCount)
  for i in range(trainDataCount):
    imageStartTime = startTimeI + (slide * i)
    #print(f"{imageStartTime - startTimeI}-{imageStartTime + imageDuration - startTimeI}")
    df1 = df[(imageStartTime < df["Timestamp"]) & (df["Timestamp"] < imageStartTime + imageDuration)]
    Generate(trainDataDirPath, df1, i)

  #print(df.head(5))

def Generate(trainDataDirPath, df, count):
  imagePath = f"{trainDataDirPath}/{count}.png"

  # if count != 1:
  #   return

  FlowPic.Generate(df, imagePath)
