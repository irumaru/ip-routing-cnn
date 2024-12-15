import UpdateRoute

currentConfig = {
  # "dst": "gateway"
  "0.0.0.0/0": "192.168.10.1",
  "123.10.0.0/32": "192.168.10.2",
  "15.0.0.1/32": "192.168.10.2"
}

UpdateRoute.UpdateRoute(currentConfig)
