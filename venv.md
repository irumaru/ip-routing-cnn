# パッケージのインストール
```
sudo apt install python3.12-venv
```

# venvのセットアップ
```
sudo python3 -m venv venv
```

# venvの起動
```
sudo -su root
source ./venv/bin/activate
```

# 必須パッケージのインストール
```
pip install -r requirements.txt
```

# NICがリンクアップしない場合
```
ip link set enx84e8cb7e1b0d up
```
