from enum import Enum

from pydantic import BaseModel


class VerificationDecision(str, Enum):

    ANSWER = "answer"

    RETRY = "retry"

    STOP = "stop"


class VerificationResult(BaseModel):

    supported: bool

    confidence: int

    reasoning: str

    missing_information: list[str]

    decision: VerificationDecision