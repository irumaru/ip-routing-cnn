# インターネット側のIPアドレスに基づき、経路を設定する

# 入力
# 1. インターネット側のIPアドレス
# 2. ゲートウェイのIPアドレス

import RouterAdaptor.vyos as rc

class Router:
  def __init__(self, routerHost):
    self.rc = rc.RouterController(hostname=routerHost)
    self.staticRoute = {}

  # 固定経路の追加
  def SetStaticRoute(self, routeList):
    self.staticRoute = routeList

  # 経路更新
  # リストの更新を適用
  def UpdateRoute(self, routeList, sourceRouteList):
    config = self.getConfig()

    newConfig = self.replaceRoute(config, routeList, sourceRouteList)

    self.saveConfig(newConfig)

  # config読み込み
  def getConfig(self):
    return self.rc.get_config()

  # configへ経路を追加
  def replaceRoute(self, config, routeList, sourceRouteList):
    # 固定経路を追加
    routeList.update(self.staticRoute)

    pb = self.rc.create_protocols_block(routeList, sourceRouteList)

    return self.rc.replace_protocols_block(config, pb)

  # config保存
  def saveConfig(self, config):
    #print(config)
    self.rc.apply_config(config)
