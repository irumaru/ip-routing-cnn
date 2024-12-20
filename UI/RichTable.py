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
    self.table.add_column("Label")

  def add(self, streamId, srcIP, srcPort, dstIP, dstPort, protocol, length, duration, label):
    self.table.add_row(str(streamId), str(srcIP), str(srcPort), str(dstIP), str(dstPort), str(protocol), str(DataSize.Print(length)), str(duration), str(label))

  def print(self):
    console = Console()
    console.print(self.table)

class TrafficMini:
  def __init__(self):
    self.table = Table(title="traffic table")
    self.table.add_column("StreamID")
    self.table.add_column("SrcIP")
    self.table.add_column("DstIP")
    self.table.add_column("Length")
    self.table.add_column("Duration")
    self.table.add_column("Predicted")
    self.table.add_column("Probabilities")

  def add(self, streamId, srcIP, dstIP, length, duration, predicted, probabilities):
    self.table.add_row(str(streamId), str(srcIP), str(dstIP), str(DataSize.Print(length)), str(format(duration, ".2f")), str(predicted), str(format(probabilities, ".2f")))

  def print(self):
    console = Console()
    console.print(self.table)
