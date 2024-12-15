from scapy.all import *
import traceback
import threading
#import multiprocessing

import DataStruct.Raw as Raw
import RawData
import ProcessCtrl

#manager = multiprocessing.Manager()
#rt = manager.list()
#rtLock = manager.Lock()

def recoder(pkt):
  if "IP" not in pkt:
    #print(f"Not IP packet")
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
    #print(f"Not TCP or UDP packet")
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

  rt = RawData.Table.getInstance().getRawTable()
  rtLock = RawData.Table.getInstance().getRawTableLock()
  with rtLock:
    rt.append(rr)
  #print(length)
  #print(f"RawTable count: {len(rt)}")


def Start():
  try:
    #sniff(iface="enx84e8cb7e1b0d", prn=recoder, store=0, filter="ip")
    t = AsyncSniffer(iface="enx84e8cb7e1b0d", prn=recoder, store=0, filter="ip")
    t.start()
    while ProcessCtrl.Runnables.getInstance().getRunnable():
      time.sleep(1)
    return
  except:
    traceback.print_exc()



def TrainStart(duration):
  try:
    #sniff(iface="enx84e8cb7e1b0d", prn=recoder, store=0, filter="ip")
    t = AsyncSniffer(iface="enx84e8cb7e1b0d", prn=recoder, store=0, filter="ip")
    t.start()
    time.sleep(duration)
    return
  except:
    traceback.print_exc()
