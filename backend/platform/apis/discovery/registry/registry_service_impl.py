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
from backend.platform.apis.service.api_service import (
    ApiService,
)


class RegistryServiceImpl(
    RegistryService,
):
    """
    Applies synchronization plans to the API registry.
    """

    def __init__(
        self,
        api_service: ApiService,
        mapper: RegistryMapper,
    ) -> None:
        self._api_service = api_service
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

                        request = self._mapper.to_create_request(
                            plan.route,
                        )

                        created_api = self._api_service.create(
                            plan.route.environment_id,
                            request,
                        )

                        applied.append(
                            plan,
                        )

                    case SyncOperation.UPDATE:

                        skipped.append(
                            plan,
                        )

                    case SyncOperation.ARCHIVE:

                        skipped.append(
                            plan,
                        )

                    case SyncOperation.UNCHANGED:

                        skipped.append(
                            plan,
                        )

            except Exception as exc:

                failed.append(
                    plan,
                )

        return SyncResult(
            applied=applied,
            skipped=skipped,
            failed=failed,
        )