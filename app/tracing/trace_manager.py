from datetime import datetime

from app.tracing.trace import TraceEvent
from app.tracing.trace_logger import TraceLogger


class TraceManager:

    def __init__(self):

        self.events = []

    def add(
        self,
        node: str,
        title: str,
        data,
    ):

        self.events.append(

            TraceEvent(

                timestamp=datetime.utcnow(),

                node=node,

                title=title,

                data=data,
            )
        )

    def save(
        self,
        trace_id: str,
    ):

        TraceLogger().write(
            trace_id,
            self.events,
        )