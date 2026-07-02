from backend.execution.bus.event_bus import EventBus


def test_event_bus_is_abstract() -> None:
    try:
        EventBus()
        assert False
    except TypeError:
        assert True