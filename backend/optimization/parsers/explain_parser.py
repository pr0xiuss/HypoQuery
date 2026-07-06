from backend.optimization.models.execution_plan import (
    ExecutionPlan,
)


class ExplainParser:

    def parse(
        self,
        explain_json: dict,
    ) -> ExecutionPlan:

        return self._parse_node(
            explain_json["Plan"],
            explain_json,
        )

    def _parse_node(
        self,
        node: dict,
        explain_json: dict,
    ) -> ExecutionPlan:

        children = []

        for child in node.get("Plans", []):

            children.append(
                self._parse_node(
                    child,
                    explain_json,
                )
            )

        return ExecutionPlan(
            node_type=node["Node Type"],
            relation_name=node.get("Relation Name"),
            schema_name=node.get("Schema"),
            alias=node.get("Alias"),
            parent_relationship=node.get("Parent Relationship"),
            join_type=node.get("Join Type"),
            index_name=node.get("Index Name"),
            hash_condition=node.get("Hash Cond"),
            filter_condition=node.get("Filter"),
            index_condition=node.get("Index Cond"),
            recheck_condition=node.get("Recheck Cond"),
            merge_condition=node.get("Merge Cond"),
            join_filter=node.get("Join Filter"),
            estimated_rows=node["Plan Rows"],
            actual_rows=node["Actual Rows"],
            startup_cost=node["Startup Cost"],
            total_cost=node["Total Cost"],
            planning_time_ms=explain_json["Planning Time"],
            execution_time_ms=explain_json["Execution Time"],
            shared_hit_blocks=node.get(
                "Shared Hit Blocks",
                0,
            ),
            shared_read_blocks=node.get(
                "Shared Read Blocks",
                0,
            ),
            temp_read_blocks=node.get(
                "Temp Read Blocks",
                0,
            ),
            temp_written_blocks=node.get(
                "Temp Written Blocks",
                0,
            ),
            children=children,
        )
