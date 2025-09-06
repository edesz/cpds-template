#!/usr/bin/env python3


"""Utility function to display test report."""

import argparse
import logging
import webbrowser
from pathlib import Path
from shutil import get_terminal_size
from typing import Union

from rich import print


def show_test_outputs(show_htmls: bool = True) -> None:
    """Show test summary report and code coverage annotated in files.

    :param show_htmls: Whether to show the test report HTML in a browser.
    """
    term_dims = get_terminal_size((80, 20))
    n_dashes, n_rem = divmod(term_dims[0], 2)
    smsg = ""
    file_print_divider = smsg.join(["=" * (n_dashes + int(n_rem / 2))] * 2)

    PROJECT_DIR = Path(__file__).parents[1]

    fpath_report_md = PROJECT_DIR / "test-logs" / "report.md"
    with fpath_report_md.open() as f:
        print(f"{f.read()}{file_print_divider}")

    logger = logging.getLogger(__name__)
    logger.info(f"Lauch HTMLs in browser = {show_htmls}")

    if show_htmls:
        test_logs_dir = PROJECT_DIR / "test-logs"
        cov_html_file_path = test_logs_dir / "htmlcov" / "index.html"
        summary_html_file_path = test_logs_dir / "testreport.html"
        for f in [summary_html_file_path, cov_html_file_path]:
            webbrowser.open_new_tab(str(f))


def str2bool(inp_value: Union[bool, str]) -> bool:
    """Convert string to boolean.

    :param inp_value: The value to be checked.
    :return: Whether the value agrees with a boolean.

    Raises:
        ArgumentTypeError: If 'inp_value' is not one of bool or string.

    """
    if isinstance(inp_value, bool):
        return inp_value
    if inp_value.lower() in ("yes", "true", "t", "y", "1"):
        return True
    if inp_value.lower() in ("no", "false", "f", "n", "0"):
        return False
    raise argparse.ArgumentTypeError("Boolean value expected.")


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--show-htmls",
        type=str2bool,
        nargs="?",
        const=True,
        dest="show_htmls",
        default=True,
        help="whether to open Test summary, Coverage HTML reports in browser",
    )
    args = parser.parse_args()
    show_test_outputs(args.show_htmls)
