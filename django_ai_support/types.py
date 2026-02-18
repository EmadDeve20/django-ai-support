from typing import TypedDict, Optional, Any, Literal

class ShortTermMemoryOptions(TypedDict, total=False):
    MIN_POOL_SIZE: Optional[int]
    MAX_POOL_SIZE: Optional[int]


class ShortTermMemoryConfig(TypedDict, total=False):
    TYPE: Literal["redis", "postgres", "mongodb"]
    URL: str
    OPTIONS: Optional[ShortTermMemoryOptions]


class AISupportSettings(TypedDict):
    TOOLS: list[Any]
    SYSTEM_PROMPT: str
    LLM_MODEL: Any
    SHORT_TERM_MEMORY: Optional[ShortTermMemoryConfig]

