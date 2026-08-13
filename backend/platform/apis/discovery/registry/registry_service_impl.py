from uuid import uuid4

from backend.platform.apis.discovery.registry.registry_mapper import (
    RegistryMapper,
)
from backend.platform.apis.discovery.registry.registry_service import (
    RegistryService,
)
from backend.platform.apis.discovery.synchronization.sync_operation import (
    SyncOperation,
)
from backend.platform.apis.discovery.synchronization.sync_plan import (
    SyncPlan,
)
from backend.platform.apis.discovery.synchronization.sync_result import (
    SyncResult,
)
from backend.platform.apis.domain.api_endpoint import (
    ApiEndpoint,
)
from backend.platform.apis.repositories.api_endpoint_repo import (
    ApiEndpointRepository,
)


class RegistryServiceImpl(
    RegistryService,
):
    """
    Applies synchronization plans to the API endpoint registry.
    """

    def __init__(
        self,
        api_endpoint_repository: ApiEndpointRepository,
        mapper: RegistryMapper,
    ) -> None:
        self._api_endpoint_repository = (
            api_endpoint_repository
        )
        self._mapper = mapper

    def apply(
        self,
        plans: list[
            SyncPlan
        ],
    ) -> SyncResult:

        applied: list[SyncPlan] = []
        skipped: list[SyncPlan] = []
        failed: list[SyncPlan] = []

        for plan in plans:

            try:

                match plan.operation:

                    case SyncOperation.CREATE:

                        if plan.route is None:
                            raise ValueError(
                                "CREATE plan requires a discovered route.",
                            )

                        request = (
                            self._mapper
                            .to_create_endpoint_request(
                                plan.route,
                            )
                        )

                        endpoint = ApiEndpoint(
                            id=uuid4(),
                            api_id=plan.api_id,
                            method=request.method,
                            path=request.path,
                            handler=request.handler,
                            source_file=request.source_file,
                            line_number=request.line_number,
                            summary=request.summary,
                            description=request.description,
                            tags=request.tags,
                            version=request.version,
                            authentication_required=(
                                request.authentication_required
                            ),
                        )

                        self._api_endpoint_repository.create(
                            endpoint,
                        )

                        applied.append(plan)

                    case SyncOperation.UPDATE:

                        if plan.route is None:
                            raise ValueError(
                                "UPDATE plan requires a discovered route.",
                            )

                        if plan.existing_endpoint_id is None:
                            raise ValueError(
                                "UPDATE plan requires an existing endpoint ID.",
                            )

                        request = (
                            self._mapper
                            .to_create_endpoint_request(
                                plan.route,
                            )
                        )

                        endpoint = ApiEndpoint(
                            id=plan.existing_endpoint_id,
                            api_id=plan.api_id,
                            method=request.method,
                            path=request.path,
                            handler=request.handler,
                            source_file=request.source_file,
                            line_number=request.line_number,
                            summary=request.summary,
                            description=request.description,
                            tags=request.tags,
                            version=request.version,
                            authentication_required=(
                                request.authentication_required
                            ),
                        )

                        self._api_endpoint_repository.update(
                            endpoint,
                        )

                        applied.append(plan)

                    case SyncOperation.ARCHIVE:

                        if plan.existing_endpoint_id is None:
                            raise ValueError(
                                "ARCHIVE plan requires an existing endpoint ID.",
                            )

                        self._api_endpoint_repository.delete(
                            plan.existing_endpoint_id,
                        )

                        applied.append(plan)

                    case SyncOperation.UNCHANGED:

                        skipped.append(plan)

            except Exception:
                failed.append(plan)

        return SyncResult(
            applied=applied,
            skipped=skipped,
            failed=failed,
        )