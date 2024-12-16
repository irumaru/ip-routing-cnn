import paramiko
from io import StringIO

#import vyosTestData

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

# コマンドの実行
def exec_command(command):
  print(f"Executing command: {command}")
  stdin, stdout, stderr = client.exec_command(command)
  
  status = stdout.channel.recv_exit_status()
  print(f"Exit status: {status}")
  print(f"STDOUT:\n{stdout.read().decode('utf-8')}\nSTDERR:\n{stderr.read().decode('utf-8')}")

  return status

# 設定ファイルの読み込み
def get_config():
  with client.open_sftp() as sftp:
    with sftp.open(saveConfigPath, "r") as file:
      return file.read().decode('utf-8')

# 設定ファイルの適用
def apply_config(config):
  # 設定ファイル書き込み
  with client.open_sftp() as sftp:
    with StringIO(config) as fileObj:
      sftp.putfo(fileObj, updateConfigPath)
  # 設定の適用
  exec_command(applyConfigCmd)

# 設定ファイルの書き換え
def replace_protocols_block(config, protocols):
  config_n = config.split("\n")
  
  exist = True

  try:
    s = config_n.index("protocols {")
  except ValueError:
    # Error: protocols block not found
    exist = False
  
  if exist:
    e = config_n.index("}", s)
    print("s: ", s, "   e: ", e)
    config_n[s:e + 1] = protocols.split("\n")
  else:
    config_n[0:0] = protocols.split("\n")

  config_new = ""
  for config_line in config_n:
    config_new += config_line + "\n"
  
  return config_new

# protocols blockの作成
def create_protocols_block(routeList, sourceRouteList):
  policy = """policy {
    route PBR {
"""

  protocols = """protocols {
    static {
"""

  # 送信元リスト
  # key + 1: Rule ID
  srcList = list(set(sourceRouteList.keys()))

  # srcごとにrule
  # dstごとにtable
  for src in srcList:
    srcId = srcList.index(src) + 1
    policy += f"""        rule {srcId} {{
            set {{
                table {srcId}
            }}
            source {{
                address {src}
            }}
        }}
"""
    protocols += f"""        table {srcId} {{
"""
    for dst in sourceRouteList[src]:
      protocols += f"""            route {dst} {{
                next-hop 192.168.8.3 {{
                }}
            }}
"""
    protocols += f"""        }}
"""

  for key, value in routeList.items():
    protocols += f"""        route {key} {{
            next-hop {value} {{
            }}
        }}
"""
  
  policy += """    }
}
"""

  protocols += """    }
}"""

  return policy + protocols

# テスト
#print(replace_protocols_block(vyosTestData.c, vyosTestData.p))
#print(create_protocols_block(vyosTestData.r))
