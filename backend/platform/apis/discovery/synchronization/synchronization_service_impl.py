from uuid import UUID

from backend.platform.apis.discovery.domain.discovered_route import (
    DiscoveredRoute,
)
from backend.platform.apis.discovery.synchronization.sync_operation import (
    SyncOperation,
)
from backend.platform.apis.discovery.synchronization.sync_plan import (
    SyncPlan,
)
from backend.platform.apis.discovery.synchronization.synchronization_service import (
    SynchronizationService,
)
from backend.platform.apis.repositories.api_endpoint_repo import (
    ApiEndpointRepository,
)


class SynchronizationServiceImpl(
    SynchronizationService,
):
    """
    Compares discovered routes against the persisted
    endpoints belonging to a specific API.
    """

    def __init__(
        self,
        api_endpoint_repository: ApiEndpointRepository,
    ) -> None:
        self._api_endpoint_repository = (
            api_endpoint_repository
        )

    def synchronize(
        self,
        environment_id: UUID,
        api_id: UUID,
        discovered_routes: list[
            DiscoveredRoute
        ],
    ) -> list[
        SyncPlan
    ]:

        existing_endpoints = (
            self._api_endpoint_repository.list_by_api(
                api_id,
            )
        )

        existing_endpoint_map = {
            (
                endpoint.method.upper(),
                endpoint.path,
            ): endpoint
            for endpoint in existing_endpoints
        }

        discovered_route_map = {
            (
                route.method.upper(),
                route.path,
            ): route
            for route in discovered_routes
        }

        plans: list[SyncPlan] = []

        for key, route in discovered_route_map.items():

            existing_endpoint = (
                existing_endpoint_map.get(key)
            )

            if existing_endpoint is None:
                plans.append(
                    SyncPlan(
                        operation=SyncOperation.CREATE,
                        api_id=api_id,
                        route=route,
                    )
                )

                continue

            if (
                existing_endpoint.handler
                != route.handler
                or existing_endpoint.summary
                != route.summary
                or existing_endpoint.description
                != route.description
                or existing_endpoint.tags
                != route.tags
                or existing_endpoint.version
                != route.version
                or (
                    existing_endpoint.authentication_required
                    != route.authentication_required
                )
            ):
                plans.append(
                    SyncPlan(
                        operation=SyncOperation.UPDATE,
                        api_id=api_id,
                        route=route,
                        existing_endpoint_id=(
                            existing_endpoint.id
                        ),
                    )
                )

            else:
                plans.append(
                    SyncPlan(
                        operation=SyncOperation.UNCHANGED,
                        api_id=api_id,
                        route=route,
                        existing_endpoint_id=(
                            existing_endpoint.id
                        ),
                    )
                )

        for key, endpoint in existing_endpoint_map.items():

            if key in discovered_route_map:
                continue

            plans.append(
                SyncPlan(
                    operation=SyncOperation.ARCHIVE,
                    api_id=api_id,
                    existing_endpoint_id=endpoint.id,
                )
            )

        return plans