class PipelineError(Exception):
    """Base exception for all pipeline-related errors."""


class PipelineExecutionError(PipelineError):
    """Raised when pipeline execution fails."""


class NodeExecutionError(PipelineError):
    """Raised when a pipeline node fails."""


class PipelineValidationError(PipelineError):
    """Raised when a pipeline definition is invalid."""