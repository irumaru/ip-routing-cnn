from rich.console import Console
from rich.table import Table

import UI.DataSize as DataSize

class Traffic:
  def __init__(self):
    self.table = Table(title="traffic table")
    self.table.add_column("StreamID")
    self.table.add_column("SrcIP")
    self.table.add_column("SrcPort")
    self.table.add_column("DstIP")
    self.table.add_column("DstPort")
    self.table.add_column("Protocol")
    self.table.add_column("Length")
    self.table.add_column("Duration")

  def add(self, streamId, srcIP, srcPort, dstIP, dstPort, protocol, length, duration):
    self.table.add_row(str(streamId), str(srcIP), str(srcPort), str(dstIP), str(dstPort), str(protocol), str(DataSize.Print(length)), str(duration))

  def print(self):
    console = Console()
    console.print(self.table)
