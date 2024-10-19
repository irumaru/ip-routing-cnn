import os
import shutil
import TrainImage

PACKET_DATA = "output/archive"
TRAIN_DATA_DIR = "output/train-data"

def Main():
  idList = os.listdir(PACKET_DATA)

  for id in idList:
    src = f"{PACKET_DATA}/{id}/current.csv"
    tar = f"{TRAIN_DATA_DIR}/{id}"

    shutil.rmtree(tar, ignore_errors=True)
    os.mkdir(tar)

    TrainImage.Create(src, tar, 60)

    #exit()

if __name__ == "__main__":
  Main()
