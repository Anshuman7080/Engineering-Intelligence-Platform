from dataclasses import dataclass
from datetime import datetime
from typing import Any

@dataclass
class TraceEvent:

    timestamp:datetime

    node:str

    title:str

    data:Any