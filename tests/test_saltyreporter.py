import sys
import pytest
from saltyreporter import main
from sys import stdout, stderr


@pytest.mark.parametrize(
    "have_argv, want_exit, want_exitcode",
    [
        pytest.param(["-h"], True, 0),
        pytest.param([], True, 2),
    ],
)
def test_argument_parsing(have_argv, want_exit, want_exitcode):
    exited = False
    try:
        args = main.parse_args(have_argv)
    except SystemExit as e:
        exited = True
        exit_code = e.code

    assert exited == want_exit
    assert exit_code == want_exitcode
