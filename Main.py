from concurrent.futures import ThreadPoolExecutor
import time
import torch.nn as nn

import ProcessCtrl
import ScanPacketFlow
import Classification

# ネットワークの定義
class Net(nn.Module):
  def __init__(self):
    super(__class__, self).__init__()
    self.relu = nn.ReLU()
    # 最大値を取得するプーリング層
    # 2x2の範囲で取得し、2ずつ移動
    self.pool = nn.MaxPool2d(2, stride=2)

    self.conv1 = nn.Conv2d(1, 10, 10, stride=5)
    self.conv2 = nn.Conv2d(10, 20, 10, stride=5)

    self.fc1 = nn.Linear(3920, 64)
    #self.fc2 = nn.Softmax(dim=1)
    self.fc2 = nn.Linear(64, 4)
  
  def forward(self, x):
    x = self.conv1(x)
    x = self.relu(x)
    x = self.pool(x)
    x = self.conv2(x)
    x = self.relu(x)
    x = self.pool(x)
    x = x.view(x.size()[0], -1)
    
    x = self.fc1(x)
    x = self.relu(x)
    x = self.fc2(x)

    return x

def Main():
  try:
    print("開始")
    with ThreadPoolExecutor() as executor:
      pr = executor.submit(ScanPacketFlow.Start)
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
