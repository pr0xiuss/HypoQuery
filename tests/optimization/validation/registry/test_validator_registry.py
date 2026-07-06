from backend.optimization.validation.registry.validator_registry import (
    ValidatorRegistry,
)
from backend.optimization.validation.validators.base_validator import (
    RecommendationValidator,
)


class DummyValidator(
    RecommendationValidator,
):

    @property
    def name(
        self,
    ) -> str:

        return "dummy"

    @property
    def supported_codes(
        self,
    ) -> set[str]:

        return {
            "CREATE_INDEX",
        }

    def validate(
        self,
        context,
        recommendation,
    ):

        return None


def test_register_validator():

    registry = ValidatorRegistry()

    validator = DummyValidator()

    registry.register(
        validator,
    )

    assert len(registry) == 1


def test_iter_registry():

    registry = ValidatorRegistry()

    validator = DummyValidator()

    registry.register(
        validator,
    )

    validators = list(
        registry,
    )

    assert validators == [
        validator,
    ]