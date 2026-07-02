from enum import Enum


class EventCategory(str, Enum):
    PIPELINE = "pipeline"
    NODE = "node"
    QUEUE = "queue"
    WORKER = "worker"


class EventVersion(str, Enum):
    V1 = "1.0"