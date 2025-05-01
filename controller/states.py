from dataclasses import dataclass
from typing import List, Optional

@dataclass
class State:
    thought: str = ""
    answer: str = ""
    iteration: int = 0

@dataclass
class RetrievalState(State):
    retrieved_docs: List[str] = None
