from lumen_models.cli import main


def test_check_licenses_command_succeeds(capsys: object) -> None:
    exit_code = main(["check-licenses"])
    assert exit_code == 0


def test_render_benchmarks_command_succeeds() -> None:
    exit_code = main(["render-benchmarks"])
    assert exit_code == 0
