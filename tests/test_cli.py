from tests.conftest import CLI


def test_help(cli: CLI) -> None:
    result = cli(["--help"])
    assert result.exit_code == 0
