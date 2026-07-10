from backend.knowledge.builders.base_builder import (
    ContextBuilder,
)


def test_context_builder_is_abstract():

    assert (
        ContextBuilder.__abstractmethods__
        is not None
    )