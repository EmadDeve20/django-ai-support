from typing import TypedDict, Optional, Any, Literal

class ShortTermMemoryOptions(TypedDict, total=False):
    min_pool_size: Optional[int]
    max_pool_size: Optional[int]


class ShortTermMemoryConfig(TypedDict, total=False):
    type: Literal["redis", "postgres", "mongodb"]
    url: str
    options: Optional[ShortTermMemoryOptions]


class AISupportSettings(TypedDict):
    TOOLS: list[Any]
    SYSTEM_PROMPT: str
    LLM_MODEL: Any
    SHORT_TERM_MEMORY: Optional[ShortTermMemoryConfig]

