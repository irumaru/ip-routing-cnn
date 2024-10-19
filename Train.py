import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import matplotlib.pyplot as plt

TRAIN_DATA_DIR = "output/train-data"

BATCH_SIZE = 100
WEIGHT_DECAY = 0.005
LEARNING_RATE = 0.0001
EPOCH = 10


# データセットの読み込み
class ImageTransform():
  def __init__(self, mean, std):
    self.data_transform = torchvision.transforms.Compose([
      torchvision.transforms.Grayscale(num_output_channels=1),
      torchvision.transforms.ToTensor(),
      torchvision.transforms.Normalize(mean, std)
    ])
  
  def __call__(self, img):
    return self.data_transform(img)

data = torchvision.datasets.ImageFolder(root=TRAIN_DATA_DIR, transform=ImageTransform(mean=(0.5,), std=(0.5,)))

# データセットを訓練用とテスト用に分割
trainSize = int(len(data) * 0.8)
testSize = len(data) - trainSize

trainData, testData = torch.utils.data.random_split(data, [trainSize, testSize])

trainLoader = torch.utils.data.DataLoader(trainData, batch_size=BATCH_SIZE, shuffle=True, pin_memory=True)
testLoader = torch.utils.data.DataLoader(testData, batch_size=BATCH_SIZE, shuffle=True, pin_memory=True)

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

# ネットワークのインスタンスを生成
device = torch.device("cuda:0")
net = Net()
net = net.to(device)

# 学習パラメーター
criterion = nn.CrossEntropyLoss()
#optimizer = optim.SGD(net.parameters(), lr=LEARNING_RATE, momentum=0.9, weight_decay=WEIGHT_DECAY)
optimizer = optim.Adam(net.parameters(), lr=LEARNING_RATE)

train_loss_value=[]      #trainingのlossを保持するlist
train_acc_value=[]       #trainingのaccuracyを保持するlist
test_loss_value=[]       #testのlossを保持するlist
test_acc_value=[]        #testのaccuracyを保持するlist 

for epoch in range(EPOCH):
  print(f"epoch: {epoch + 1}")
  
  for (inputs, labels) in trainLoader:
    inputs, labels = inputs.to(device), labels.to(device)
    optimizer.zero_grad()
    outputs = net(inputs)
    loss = criterion(outputs, labels)
    loss.backward()
    optimizer.step()

  sum_loss = 0.0
  sum_correct = 0
  sum_total = 0

  #train dataを使ってテストをする(パラメータ更新がないようになっている)
  for (inputs, labels) in trainLoader:
    inputs, labels = inputs.to(device), labels.to(device)
    optimizer.zero_grad()
    outputs = net(inputs)
    loss = criterion(outputs, labels)
    sum_loss += loss.item()                            #lossを足していく
    _, predicted = outputs.max(1)                      #出力の最大値の添字(予想位置)を取得
    sum_total += labels.size(0)                        #labelの数を足していくことでデータの総和を取る
    sum_correct += (predicted == labels).sum().item()  #予想位置と実際の正解を比べ,正解している数だけ足す
  print("train mean loss={}, accuracy={}"
          .format(sum_loss*BATCH_SIZE/len(trainLoader.dataset), float(sum_correct/sum_total)))  #lossとaccuracy出力
  train_loss_value.append(sum_loss*BATCH_SIZE/len(trainLoader.dataset))  #traindataのlossをグラフ描画のためにlistに保持
  train_acc_value.append(float(sum_correct/sum_total))   #traindataのaccuracyをグラフ描画のためにlistに保持

  sum_loss = 0.0
  sum_correct = 0
  sum_total = 0

  #test dataを使ってテストをする
  for (inputs, labels) in testLoader:
    inputs, labels = inputs.to(device), labels.to(device)
    optimizer.zero_grad()
    outputs = net(inputs)
    loss = criterion(outputs, labels)
    sum_loss += loss.item()
    _, predicted = outputs.max(1)
    sum_total += labels.size(0)
    sum_correct += (predicted == labels).sum().item()
  print("test  mean loss={}, accuracy={}"
          .format(sum_loss*BATCH_SIZE/len(testLoader.dataset), float(sum_correct/sum_total)))
  test_loss_value.append(sum_loss*BATCH_SIZE/len(testLoader.dataset))
  test_acc_value.append(float(sum_correct/sum_total))

torch.save(net, "output/train/model.pth")  #モデルの保存
# model = torch.load('model_weight.pth')

plt.figure(figsize=(6,6))      #グラフ描画用

#以下グラフ描画
plt.plot(range(EPOCH), train_loss_value)
plt.plot(range(EPOCH), test_loss_value, c='#00ff00')
plt.xlim(0, EPOCH)
plt.ylim(0, 2.5)
plt.xlabel('EPOCH')
plt.ylabel('LOSS')
plt.legend(['train loss', 'test loss'])
plt.title('loss')
plt.savefig("output/train/loss_image.png")
plt.clf()

plt.plot(range(EPOCH), train_acc_value)
plt.plot(range(EPOCH), test_acc_value, c='#00ff00')
plt.xlim(0, EPOCH)
plt.ylim(0, 1)
plt.xlabel('EPOCH')
plt.ylabel('ACCURACY')
plt.legend(['train acc', 'test acc'])
plt.title('accuracy')
plt.savefig("output/train/accuracy_image.png")
