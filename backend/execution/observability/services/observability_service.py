from psycopg import Connection

from infrastructure.postgres.scripts.observability.collectors.explain_collector import (
    ExplainCollector,
)
from infrastructure.postgres.scripts.observability.collectors.metrics_collector import (
    MetricsCollector,
)
from infrastructure.postgres.scripts.observability.parsers.explain_parser import (
    ExplainParser,
)
from infrastructure.postgres.scripts.observability.analyzers.plan_analyzer import (
    PlanAnalyzer,
)

# from infrastructure.postgres.scripts.observability.services.optimization_pipeline_service import (
#     OptimizationPipelineService,
# )


class ObservabilityService:

    def __init__(self, connection: Connection):

        self.explain = ExplainCollector(connection)
        self.metrics = MetricsCollector(connection)
        self.parser = ExplainParser()
        self.analyzer = PlanAnalyzer()
        # self.pipeline = OptimizationPipelineService(connection)

    def collect_plan(
        self,
        sql: str,
    ):

        explain_json = self.explain.collect(sql)

        execution_plan = self.parser.parse(explain_json)

        return execution_plan

    def analyze_query(
        self,
        query,
    ):

        plan = self.collect_plan(query.sql)

        findings = self.analyzer.analyze(plan)

        return plan, findings
