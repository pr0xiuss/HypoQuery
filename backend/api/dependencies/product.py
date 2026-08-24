from fastapi import Request

from backend.api.dependencies.container import get_container
from backend.assistant.api.assistant_service_facade import AssistantServiceFacade
from backend.knowledge.service import ContextService, ExplanationService
from backend.product.dashboard.dashboard_service import DashboardService
from backend.product.workloads.workload_service import WorkloadService
from backend.product.queries.query_service import QueryService
from backend.product.operations.operations_service import OperationsService


def get_assistant_facade(request: Request) -> AssistantServiceFacade:
    container = get_container(request)
    return container.assistant_service_facade()

def get_context_service(request: Request) -> ContextService:
    container = get_container(request)
    return container.context_service()

def get_explanation_service(request: Request) -> ExplanationService:
    container = get_container(request)
    return container.explanation_service()

def get_dashboard_service(request: Request) -> DashboardService:
    container = get_container(request)
    return container.dashboard_service()

def get_workload_service(request: Request) -> WorkloadService:
    container = get_container(request)
    return container.workload_service()

def get_query_service(request: Request) -> QueryService:
    container = get_container(request)
    return container.query_service()

def get_operations_service(request: Request) -> OperationsService:
    container = get_container(request)
    return container.operations_service()
