# インターネット側のIPアドレスに基づき、経路を設定する

# 入力
# 1. インターネット側のIPアドレス
# 2. ゲートウェイのIPアドレス

import RouterAdaptor.vyos as rc


# 経路更新
# リストの更新を適用
def UpdateRoute(routeList, sourceRouteList):
  config = getConfig()

  newConfig = replaceRoute(config, routeList, sourceRouteList)

  saveConfig(newConfig)

# config読み込み
def getConfig():
  return rc.get_config()

# configへ経路を追加
def replaceRoute(config, routeList, sourceRouteList):
  # 固定経路を追加
  routeList["0.0.0.0/0"] = "192.168.9.2"

  pb = rc.create_protocols_block(routeList, sourceRouteList)

  return rc.replace_protocols_block(config, pb)

# config保存
def saveConfig(config):
  print(config)
  #rc.apply_config(config)
