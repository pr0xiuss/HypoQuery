from __future__ import annotations

from psycopg import Connection

from backend.execution.pipeline.builder import PipelineBuilder
from backend.execution.pipeline.definition import (
    NodeDefinition,
    PipelineDefinition,
)
from backend.optimization.analysis.composition import build_analysis_engine

from backend.execution.pipeline.pipeline import Pipeline
from backend.execution.pipeline.registry import NodeRegistry

from backend.optimization.collectors.explain_collector import ExplainCollector
from backend.optimization.nodes.explain_collect_node import (
    ExplainCollectNode,
)
from backend.optimization.nodes.explain_parse_node import (
    ExplainParseNode,
)
from backend.optimization.nodes.fingerprint_node import (
    FingerprintNode,
)
from backend.optimization.nodes.normalize_node import (
    NormalizeNode,
)
from backend.optimization.nodes.plan_analyze_node import (
    PlanAnalyzeNode,
)
from backend.optimization.parsers.explain_parser import ExplainParser


class OptimizationPipelineBuilder:
    """
    Builds the deterministic optimization pipeline.

    Phase 1 becomes a reusable execution pipeline.
    """

    def __init__(
        self,
        connection: Connection,
    ) -> None:

        self._connection = connection

    def build(self) -> Pipeline:

        registry = NodeRegistry()

        explain_collector = ExplainCollector(
            self._connection,
        )

        explain_parser = ExplainParser()

        analysis_engine = build_analysis_engine()

        registry.register(
            NormalizeNode(),
        )

        registry.register(
            FingerprintNode(),
        )

        registry.register(
            ExplainCollectNode(
                explain_collector,
            )
        )

        registry.register(
            ExplainParseNode(
                explain_parser,
            )
        )

        registry.register(
            PlanAnalyzeNode(
                analysis_engine,
            )
        )

        definition = PipelineDefinition(
            pipeline_id="optimization",
            version="1.0",
            description="Deterministic SQL Optimization Pipeline",
            entry_node="normalize",
            nodes=(
                NodeDefinition("normalize"),
                NodeDefinition("fingerprint"),
                NodeDefinition("explain_collect"),
                NodeDefinition("explain_parse"),
                NodeDefinition("plan_analyze"),
            ),
            edges={
                "normalize": ("fingerprint",),
                "fingerprint": ("explain_collect",),
                "explain_collect": ("explain_parse",),
                "explain_parse": ("plan_analyze",),
            },
        )

        return PipelineBuilder(
            registry,
        ).build(
            definition,
        )