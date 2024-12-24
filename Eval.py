from PIL import Image
#import torchvision.transforms as transforms
import torchvision
import torch
import torch.nn.functional as F

# 定義済みネットワークの読み込み
from Net import Net

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
    device = torch.device("cpu")
    model = model.to(device)

    # モデルの評価モードに切り替え
    model.eval()
    
    # 画像の前処理
    img_tensor = preprocess_image(image_path)
    img_tensor = img_tensor.to(device)
    
    # 予測
    with torch.no_grad():
        output = model(img_tensor)
        
        modelProbabilities = F.softmax(output, dim=1)
        probabilities, predicted = torch.max(modelProbabilities, 1)
        print(f"Probabilities: {modelProbabilities}, {probabilities}, {predicted}")
    
    # 予測結果の表示
    return {
        "predicted": predicted.item(),
        "probabilities": probabilities.item()
    }

def Eval(image_path):
  # モデルの読み込み
  MODEL_PATH = "output/train/model.pth"
  # loaded_net = Net()
  # loaded_net.load_state_dict(torch.load(MODEL_PATH))
  loaded_net = torch.load(MODEL_PATH, torch.device('cpu'), weights_only=False)

  # 判定する画像のパス
  #image_path = "output/train-data/discord-server-video/7.png"

  # 画像の判定
  predict = predict_image(image_path, loaded_net)
  #print(f"Predicted Label: {predicted_label}")
  return predict

# if __name__ == "__main__":
#   print(Eval())
