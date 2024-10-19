from PIL import Image
import torchvision.transforms as transforms
import torchvision
import torch
import torch.nn as nn

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

# 画像の前処理
def preprocess_image(image_path):
    transform = ImageTransform(mean=(0.5,), std=(0.5,))
    img = Image.open(image_path).convert('L')  # 画像をグレースケールに変換
    img = transform(img)
    img = img.unsqueeze(0)  # バッチサイズを1に
    return img

# 画像の判定関数
def predict_image(image_path, model):
    # ネットワークのインスタンスを生成
    device = torch.device("cuda:0")
    model = model.to(device)

    # モデルの評価モードに切り替え
    model.eval()
    
    # 画像の前処理
    img_tensor = preprocess_image(image_path)
    img_tensor = img_tensor.to(device)
    
    # 予測
    with torch.no_grad():
        output = model(img_tensor)
        _, predicted = output.max(1)
    
    # 予測結果の表示
    return predicted.item()

def Eval(image_path):
  # モデルの読み込み
  MODEL_PATH = "output/train/model.pth"
  # loaded_net = Net()
  # loaded_net.load_state_dict(torch.load(MODEL_PATH))
  loaded_net = torch.load(MODEL_PATH)

  # 判定する画像のパス
  #image_path = "output/train-data/discord-server-video/7.png"

  # 画像の判定
  predicted_label = predict_image(image_path, loaded_net)
  #print(f"Predicted Label: {predicted_label}")
  return predicted_label

# if __name__ == "__main__":
#   print(Eval())
