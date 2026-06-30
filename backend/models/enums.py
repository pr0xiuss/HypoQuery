from enum import Enum


class QueryCategory(Enum):

    SEQUENTIAL_SCAN = "Sequential Scan"

    JOIN = "Join"

    AGGREGATION = "Aggregation"

    SORTING = "Sorting"

    JSONB = "JSONB"

    SUBQUERY = "Subquery"

    INDEXING = "Indexing"


class Difficulty(Enum):

    EASY = "Easy"

    MEDIUM = "Medium"

    HARD = "Hard"


class ExpectedIssue(Enum):

    SEQUENTIAL_SCAN = "Sequential Scan"

    NESTED_LOOP = "Nested Loop"

    HASH_JOIN = "Hash Join"

    MERGE_JOIN = "Merge Join"

    MISSING_INDEX = "Missing Index"

    BITMAP_SCAN = "Bitmap Scan"

    SORT = "Sort"

    HASH_AGGREGATE = "Hash Aggregate"

    JSONB_SCAN = "JSONB Scan"

    SUBQUERY = "Subquery"

    CORRELATED_SUBQUERY = "Correlated Subquery"


class QueryType(Enum):

    SELECT = "SELECT"

    JOIN = "JOIN"

    INSERT = "INSERT"

    UPDATE = "UPDATE"

    DELETE = "DELETE"

    OTHER = "OTHER"


class ClassifierRoute(Enum):

    INDEX_SUGGESTER = "INDEX_SUGGESTER"

    JOIN_REORDER = "JOIN_REORDER"

    LOCK_ANALYZER = "LOCK_ANALYZER"


class PipelineStatus(Enum):

    RUNNING = "RUNNING"

    SUCCESS = "SUCCESS"

    FAILED = "FAILED"

    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"

    VALIDATION_FAILED = "VALIDATION_FAILED"


class LogLevel(Enum):

    DEBUG = "DEBUG"

    INFO = "INFO"

    WARNING = "WARNING"

    ERROR = "ERROR"

    CRITICAL = "CRITICAL"


class RemediationType(Enum):

    INDEX = "INDEX"

    QUERY_REWRITE = "QUERY_REWRITE"

    CONFIGURATION = "CONFIGURATION"

    PARTITIONING = "PARTITIONING"

    MULTIPLE = "MULTIPLE"


class ValidationStatus(Enum):

    PENDING = "PENDING"

    PASSED = "PASSED"

    FAILED = "FAILED"

    PARTIALLY_PASSED = "PARTIALLY_PASSED"


class LLMConfidence(Enum):

    LOW = "LOW"

    MEDIUM = "MEDIUM"

    HIGH = "HIGH"
