from pydantic import BaseModel
from typing import List

class DashboardStatsDTO(BaseModel):
    total_workloads: int
    active_queries: int
    optimizations_applied: int

class DashboardResponse(BaseModel):
    stats: DashboardStatsDTO
