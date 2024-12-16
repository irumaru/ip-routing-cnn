import paramiko
from io import StringIO

#import vyosTestData

class RouterController:
  def __init__(self, hostname, username="vyos", password="vyos"):
    self.client = paramiko.SSHClient()
    self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    self.updateConfigPath = "/config/config.update"
    self.saveConfigPath = "/config/config.boot"
    self.applyConfigCmd = """source /opt/vyatta/etc/functions/script-template
    configure
    load /config/config.update
    commit
    save
    """

    try:
        self.client.connect(hostname=hostname, username=username, password=password)
        print(f"{hostname}に接続しました。")
    except paramiko.AuthenticationException:
        print("認証に失敗しました。ユーザー名とパスワードを確認してください。")
    except paramiko.SSHException as ssh_exception:
        print(f"SSH接続エラー: {ssh_exception}")

  # コマンドの実行
  def exec_command(self, command):
    print(f"Executing command: {command}")
    stdin, stdout, stderr = self.client.exec_command(command)
    
    status = stdout.channel.recv_exit_status()
    print(f"Exit status: {status}")
    print(f"STDOUT:\n{stdout.read().decode('utf-8')}\nSTDERR:\n{stderr.read().decode('utf-8')}")

    return status

  # 設定ファイルの読み込み
  def get_config(self):
    with self.client.open_sftp() as sftp:
      with sftp.open(self.saveConfigPath, "r") as file:
        return file.read().decode('utf-8')

  # 設定ファイルの適用
  def apply_config(self, config):
    # 設定ファイル書き込み
    with self.client.open_sftp() as sftp:
      with StringIO(config) as fileObj:
        sftp.putfo(fileObj, self.updateConfigPath)
    # 設定の適用
    self.exec_command(self.applyConfigCmd)

  # 設定ファイルの書き換え
  def replace_protocols_block(self, config, protocols):
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
  def create_protocols_block(self, routeList, sourceRouteList):
    policy = """policy {
    route PBR {
        interface eth0
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
