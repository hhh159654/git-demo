from autoresearch_platform.stages import STAGES, by_number


def test_stage_numbers_are_contiguous() -> None:
    assert [stage.number for stage in STAGES] == list(range(1, 17))


def test_expected_gates() -> None:
    assert [stage.number for stage in STAGES if stage.gate] == [5, 8, 10]


def test_lookup() -> None:
    assert by_number(8).command == "reproduce"
