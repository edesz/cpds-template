#!/usr/bin/env python3


"""Run Jupyter notebooks."""

import copy
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Annotated

import papermill as pm
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.dataset as ds
import pytz
import typer
from nbconvert import HTMLExporter
from nbformat import read


def convert_nb_to_html(notebook_path: Path) -> None:
    """Convert Jupyter notebook to HTML.

    :param notebook_path: path of notebook to be converted to HTML.
    """
    with notebook_path.open(encoding="utf-8") as f:
        notebook_content = read(f, as_version=4)

    output_path = Path(str(notebook_path).replace("ipynb", "html"))
    html_exporter = HTMLExporter()
    (body, _) = html_exporter.from_notebook_node(notebook_content)
    with output_path.open(mode="w", encoding="utf-8") as f:
        f.write(body)
    print(f"Exported {notebook_path.name} to {output_path.name}")


def papermill_run_notebook(
    nb_dict: dict, nb_input_dir: Path, nb_output_dir: Path
) -> None:
    """Execute notebook with papermill.

    :param nb_dict: dict of params needed to run a single notebook.
    """
    for notebook, nb_params in nb_dict.items():
        now = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_nb = nb_output_dir / str(notebook.name).replace(
            ".ipynb", f"-{now}.ipynb"
        )
        print(
            f"\nInput notebook path: {notebook}",
            f"Output notebook path: {output_nb} ",
            sep="\n",
        )
        os.chdir(nb_input_dir)
        pm.execute_notebook(
            input_path=notebook,
            output_path=output_nb,
            parameters=json.loads(nb_params),
        )
        convert_nb_to_html(output_nb)


def run_notebooks(
    notebook_list: list, nb_input_dir: Path, nb_output_dir: Path
) -> None:
    """Execute notebooks from CLI."""
    for nb in notebook_list:
        papermill_run_notebook(
            nb_dict=nb, nb_input_dir=nb_input_dir, nb_output_dir=nb_output_dir
        )


def main(
    nb_nums: Annotated[
        str, typer.Argument(help="Comma-separated prefix of notebooks to run")
    ] = "01,02,03",
) -> None:
    """Execute notebooks in one or more workflow steps."""
    start_ts = datetime.now(pytz.timezone("US/Eastern"))
    print(f"Started at: {start_ts.strftime('%Y-%m-%d %H:%M:%S')}")

    PROJ_ROOT = Path.cwd()
    nbs_dir = PROJ_ROOT / "notebooks"
    nb_dir_output = PROJ_ROOT / "executed-notebooks"

    nb_paths = sorted(list(nbs_dir.glob("*.ipynb")))

    nb_parm_01 = dict(a=1)

    nb_list = [
        {"prefix": "01", "path": str(nb_paths[0]), "params": nb_parm_01},
    ]
    # convert value of params key to json object (without this, pyarrow
    # makes all rows of the params column have the same keys)
    for item in nb_list:
        if "params" in item:
            item["params"] = json.dumps(item["params"])

    # Convert list of records into pyarrow table
    pa_table = pa.Table.from_pylist(nb_list)

    # Create a pyarrow filter condition for each partial string
    filters = [
        pc.match_substring(pa_table["prefix"], substring)
        for substring in nb_nums.split(",")
    ]

    # Combine the filters using logical OR
    combined_filter = filters[0]
    for f in filters[1:]:
        combined_filter = pc.or_(combined_filter, f)

    # Apply the filter to the pyarrow table and convert to dataset
    ds_filtered = ds.InMemoryDataset(pa_table.filter(combined_filter))

    # Create list of filtered records by iterating over batches in dataset
    nb_list_filtered = [
        {Path(row["path"]): row["params"]}
        for batch in ds_filtered.to_batches()
        for row in batch.to_pylist()
    ]

    run_notebooks(nb_list_filtered, nbs_dir, nb_dir_output)
    end_ts = datetime.now(pytz.timezone("US/Eastern"))
    elapsed = (end_ts - start_ts).seconds
    print(f"Ended at: {end_ts.strftime('%Y-%m-%d %H:%M:%S')} ({elapsed}s)")


if __name__ == "__main__":
    typer.run(main)
