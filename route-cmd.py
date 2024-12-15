# インターネット側のIPアドレスに基づき、経路を設定する

# 入力
# 1. インターネット側のIPアドレス
# 2. ゲートウェイのIPアドレス

import json
from io import StringIO
import paramiko
import vyos

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

updateConfigPath = "/config/config.update"
saveConfigPath = "/config/config.boot"
applyConfigCmd = """source /opt/vyatta/etc/functions/script-template
configure
load /config/config.update
commit
save
"""

hostname = "192.168.10.11"
username = "vyos"
password = "vyos"

try:
    client.connect(hostname=hostname, username=username, password=password)
    print(f"{hostname}に接続しました。")
except paramiko.AuthenticationException:
    print("認証に失敗しました。ユーザー名とパスワードを確認してください。")
except paramiko.SSHException as ssh_exception:
    print(f"SSH接続エラー: {ssh_exception}")

currentConfig = {
  # "dst": "gateway"
  "0.0.0.0/0": "192.168.10.1",
  "123.10.0.0/32": "192.168.10.2",
  "15.0.0.1/32": "192.168.10.2"
}

env = "prod"
devConfig = "route-config.json"

def exec_command(command):
  print(f"Executing command: {command}")
  stdin, stdout, stderr = client.exec_command(command)
  
  status = stdout.channel.recv_exit_status()
  print(f"Exit status: {status}")
  print(f"STDOUT:\n{stdout.read().decode('utf-8')}\nSTDERR:\n{stderr.read().decode('utf-8')}")

  return status

# 経路更新
# リストの更新を適用
def UpdateRoute():
  config = getConfig()

  newConfig = replaceRoute(config, currentConfig)

  saveConfig(newConfig)

# config読み込み
def getConfig():
  if env == "dev":
    with open(devConfig) as f:
      return json.load(f)
  else:
    with client.open_sftp() as sftp:
      with sftp.open(saveConfigPath, "r") as file:
        return file.read().decode('utf-8')


# configへ経路を追加
def replaceRoute(config, currentConfig):
  pb = vyos.create_protocols_block(currentConfig)

  return vyos.replace_protocols_block(config, pb)

# config保存
def saveConfig(config):
  # 設定のデバッグ
  if env == "dev":
    print(json.dumps(config, indent=4))
  else:
    # 設定ファイル書き込み
    with client.open_sftp() as sftp:
      with StringIO(config) as fileObj:
        sftp.putfo(fileObj, updateConfigPath)
    # 設定の適用
    exec_command(applyConfigCmd)

#UpdateRoute()
print(UpdateRoute())
