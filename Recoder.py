from scapy.all import *
import traceback
import threading

import DataStruct.Raw as Raw

rt = Raw.RawTable([])
rtLock = threading.Lock()

def recoder(pkt):
  global rt

  if "IP" not in pkt:
    print(f"Not IP packet")
    return

  srcIp = pkt["IP"].src
  dstIp = pkt["IP"].dst

  if "TCP" in pkt:
    protocol = "TCP"
    srcPort = pkt["IP"]["TCP"].sport
    dstPort = pkt["IP"]["TCP"].dport
  elif "UDP" in pkt:
    protocol = "UDP"
    srcPort = pkt["IP"]["UDP"].sport
    dstPort = pkt["IP"]["UDP"].dport
  else:
    print(f"Not TCP or UDP packet")
    return
  
  length = pkt.len

  ts = pkt.time

  rr: Raw.RawRecord = {
    "SrcIP": srcIp,
    "DstIP": dstIp,
    "SrcPort": srcPort,
    "DstPort": dstPort,
    "Protocol": protocol,
    "Length": length,
    "Timestamp": ts
  }
  with rtLock:
    rt.append(rr)
  print(length)
  #print(f"RawTable count: {len(rt)}")


def Start():
  try:
    sniff(iface="eth0", prn=recoder)
  except:
    traceback.print_exc()
