import UpdateRoute

routeList = {
  # "dst": "gateway"
  "0.0.0.0/0": "192.168.10.1",
  "123.10.0.0/32": "192.168.10.2",
  "15.0.0.1/32": "192.168.10.2"
}

sourceRouteList = {
  # "src": "dst"
  "125.1.1.2/32": ["192.168.11.102/32"],
  "12.1.0.2/32": ["192.168.11.102/32", "192.168.11.105/32"]
}

#print(list(set(sourceRouteList.keys())))
#UpdateRoute.UpdateRoute(routeList, sourceRouteList)
router1 = UpdateRoute.Router("192.168.10.14")
router1.UpdateRoute(routeList, sourceRouteList)
