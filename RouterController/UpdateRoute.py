# インターネット側のIPアドレスに基づき、経路を設定する

# 入力
# 1. インターネット側のIPアドレス
# 2. ゲートウェイのIPアドレス

import adaptor.vyos as rc


# 経路更新
# リストの更新を適用
def UpdateRoute(routeList):
  config = getConfig()

  newConfig = replaceRoute(config, routeList)

  saveConfig(newConfig)

# config読み込み
def getConfig():
  return rc.get_config()

# configへ経路を追加
def replaceRoute(config, currentConfig):
  pb = rc.create_protocols_block(currentConfig)

  return rc.replace_protocols_block(config, pb)

# config保存
def saveConfig(config):
  rc.apply_config(config)