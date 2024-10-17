from typing import NewType
import pandas as pd

RawRecord = NewType('RawData', dict["SrcIP": str, "DstIP": str, "SrcPort": int, "DstPort": int, "Protocol": str, "Length": int, "Timestamp": float])
RawTable = NewType('RawTable', list[RawRecord])
