from uuid import UUID
from backend.platform.apis.discovery.domain.discovered_route import DiscoveredRoute
from backend.platform.apis.discovery.synchronization.sync_operation import SyncOperation
from backend.platform.apis.discovery.synchronization.sync_plan import SyncPlan
from backend.platform.apis.discovery.synchronization.synchronization_service import SynchronizationService
from backend.platform.apis.repositories.api_repo import ApiRepository


class SynchronizationServiceImpl(
    SynchronizationService,
):
    """
    Temporary synchronization implementation.

    Every discovered route is currently treated
    as a CREATE operation.

    Later this service will compare discovered
    routes against the persisted API registry.
    """
    def __init__(
        self,
        api_repository: ApiRepository,
    ) -> None:
        """
        Initializes the synchronization service.
        """

        self._api_repository = api_repository

    def synchronize(
        self,
        environment_id: UUID,
        discovered_routes: list[
            DiscoveredRoute
        ],
    ) -> list[
        SyncPlan
    ]:
        existing_apis = self._api_repository.list_by_environment(
            environment_id,
        )
        existing_api_map = {
            (
                api.method.upper(),
                api.path,
            ): api
            for api in existing_apis
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

            existing_api = existing_api_map.get(
                key,
            )

            if existing_api is None:

                plans.append(
                    SyncPlan(
                        operation=SyncOperation.CREATE,
                        route=route,
                    )
                )

                continue

            if (
                existing_api.name != route.name
                or existing_api.description != route.description
                or existing_api.framework != route.framework
            ):

                plans.append(
                    SyncPlan(
                        operation=SyncOperation.UPDATE,
                        route=route,
                        existing_api_id=existing_api.id,
                    )
                )

            else:

                plans.append(
                    SyncPlan(
                        operation=SyncOperation.UNCHANGED,
                        route=route,
                        existing_api_id=existing_api.id,
                    )
                )

            for key, api in existing_api_map.items():

                if key in discovered_route_map:
                    continue

                plans.append(
                    SyncPlan(
                        operation=SyncOperation.ARCHIVE,
                        existing_api_id=api.id,
                    )
                )