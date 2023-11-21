import sys
import pytest
from saltyreporter import main
from sys import stdout, stderr


@pytest.mark.parametrize(
    "have_argv, want_exit, want_exitcode",
    [
        pytest.param(["-h"], True, 0),
        pytest.param([], True, 2),
        pytest.param(["-d", ".", "-s", "sampleinfo.json", "-o", "basename"], False, 0),
        pytest.param(
            ["-j", "jasenreport.json", "-s", "sampleinfo.json", "-o", "basename"],
            False,
            0,
        ),
        pytest.param(
            [
                "-d",
                ".",
                "-j",
                "jasenreport.json",
                "-s",
                "sampleinfo.json",
                "-o",
                "basename",
            ],
            True,
            1,
        ),
        pytest.param(["-s", "sampleinfo.json", "-o", "basename"], True, 1),
    ],
)
def test_argument_parsing(have_argv, want_exit, want_exitcode):
    exited = False
    exit_code = 0  # Should be the default when no premature exit has happened
    try:
        args = main.parse_args(have_argv)
    except SystemExit as e:
        exited = True
        exit_code = e.code

    assert exited == want_exit
    if exited:
        assert exit_code == want_exitcode
