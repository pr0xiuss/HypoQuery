from infrastructure.postgres.scripts.observability.models.execution_plan import (
    ExecutionPlan,
)


class ExplainParser:

    def parse(
        self,
        explain_json: dict,
    ) -> ExecutionPlan:

        plan = explain_json["Plan"]

        return ExecutionPlan(

            node_type=plan["Node Type"],

            estimated_rows=plan["Plan Rows"],

            actual_rows=plan["Actual Rows"],

            startup_cost=plan["Startup Cost"],

            total_cost=plan["Total Cost"],

            planning_time_ms=explain_json["Planning Time"],

            execution_time_ms=explain_json["Execution Time"],

            shared_hit_blocks=plan["Shared Hit Blocks"],

            shared_read_blocks=plan["Shared Read Blocks"],

            temp_read_blocks=plan["Temp Read Blocks"],

            temp_written_blocks=plan["Temp Written Blocks"],
        )