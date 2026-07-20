import json
from pathlib import Path

from app.tracing.trace import TraceEvent


class TraceLogger:

    def __init__(self):

        self.directory = Path("logs/workflows")

        self.directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def write(
        self,
        trace_id: str,
        events: list[TraceEvent],
    ):

        file = self.directory / f"{trace_id}.log"

        with open(
            file,
            "w",
            encoding="utf-8",
        ) as f:

            for event in events:

                f.write("=" * 80 + "\n")

                f.write(
                    f"{event.timestamp.isoformat()}\n"
                )

                f.write(
                    f"NODE : {event.node}\n"
                )

                f.write(
                    f"TITLE: {event.title}\n\n"
                )

                if isinstance(event.data, (dict, list)):

                    f.write(
                        json.dumps(
                            event.data,
                            indent=4,
                            default=str,
                        )
                    )

                else:

                    f.write(str(event.data))

                f.write("\n\n")