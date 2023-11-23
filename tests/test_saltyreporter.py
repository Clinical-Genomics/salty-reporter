import os
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


def test_read_folder_with_input_files():
    testreports_dir = ".testreports"
    args = main.parse_args(
        [
            "-d",
            testreports_dir,
            "-s",
            f"{testreports_dir}/sampleinfo.json",
            "-o",
            testreports_dir,
        ]
    )
    os.makedirs(testreports_dir, exist_ok=True)
    for i in range(3):
        with open(f"{testreports_dir}/testreport_{i}.json", "w") as tr:
            tr.write("{}\n")
        with open(f"{testreports_dir}/sampleinfo.json", "w") as si:
            si.write("{}\n")

    main.process_reports(args)
