import pytest

from backend.execution.demo.end_node import EndNode
from backend.execution.demo.middle_node import MiddleNode
from backend.execution.demo.start_node import StartNode
from backend.execution.pipeline.registry import NodeRegistry


def test_register_node():

    registry = NodeRegistry()

    registry.register(StartNode())

    assert registry.contains("start")


def test_duplicate_registration():

    registry = NodeRegistry()

    registry.register(StartNode())

    with pytest.raises(ValueError):
        registry.register(StartNode())


def test_get_node():

    registry = NodeRegistry()

    registry.register(MiddleNode())

    node = registry.get("middle")

    assert node.name == "middle"


def test_unknown_node():

    registry = NodeRegistry()

    with pytest.raises(ValueError):
        registry.get("unknown")


def test_registered_names():

    registry = NodeRegistry()

    registry.register(StartNode())
    registry.register(MiddleNode())
    registry.register(EndNode())

    assert set(registry.names()) == {
        "start",
        "middle",
        "end",
    }