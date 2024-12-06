# インターネット側のIPアドレスに基づき、経路を設定する

# 入力
# 1. インターネット側のIPアドレス
# 2. ゲートウェイのIPアドレス

import json

currentConfig = {
  # "dst": "gateway"
  "0.0.0.0/0": "192.168.10.1",
  "135.1.0.15/32": "192.168.10.2"
}

env = "dev"
devConfig = "route-config.json"

# 経路更新
# リストの更新を適用
def UpdateRoute():
  config = getConfig()

  newConfig = addRoute(config, currentConfig)

  saveConfig(newConfig)

# config読み込み
def getConfig():
  if env == "dev":
    with open(devConfig) as f:
      return json.load(f)

# configへ経路を追加
def addRoute(config, currentConfig):
  # 経路のみ初期化
  config["protocols"]["static"]["route"] = {}

  # 経路追加
  for key, value in currentConfig.items():
    config["protocols"]["static"]["route"][key] = {
      "next-hop": {
        value: {}
      }
    }
  
  return config

# config保存
def saveConfig(config):
  # 設定のデバッグ
  if env == "dev":
    print(json.dumps(config, indent=4))
  
  # 設定書き込み

UpdateRoute()
