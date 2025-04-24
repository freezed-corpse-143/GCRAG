from dataclasses import dataclass
from typing import List, Optional

@dataclass
class State:
    """基础状态类"""
    original_question: str = ""
    current_hypothesis: str = ""
    iteration: int = 0

@dataclass
class InitialState(State):
    """初始状态，只有原始问题"""
    current_hypothesis: str = ""

@dataclass
class SubquestionState(State):
    """子问题生成状态"""
    subquestion: str = ""
    previous_hypothesis: Optional[str] = None


@dataclass
class RetrievalState(State):
    """检索状态"""
    subquestion: str = ""
    retrieved_documents: List[str] = None
    previous_hypothesis: Optional[str] = None

@dataclass
class FinalState(State):
    """最终状态"""
    subquestions: List[str] = None
    retrieved_documents: List[List[str]] = None
    all_hypotheses: List[str] = None
