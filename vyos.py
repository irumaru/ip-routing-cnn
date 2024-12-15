import vyosTestData

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
def create_protocols_block(currentConfig):
  protocols = """protocols {
    static {
"""

  for key, value in currentConfig.items():
    protocols += f"""        route {key} {{
            next-hop {value} {{
            }}
        }}
"""
  
  protocols += """    }
}"""

  return protocols

#print(replace_protocols_block(vyosTestData.c, vyosTestData.p))

#print(create_protocols_block(vyosTestData.r))
