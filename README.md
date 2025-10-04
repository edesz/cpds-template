# Python Data Analysis Template

This project uses [copier](https://copier.readthedocs.io/en/stable/) to provide an opinionated template for Python data science projects using Jupyter notebooks. This template is based on the [cookiecutter-data-science template](https://github.com/drivendataorg/cookiecutter-data-science/tree/master/%7B%7B%20cookiecutter.repo_name%20%7D%7D).

![Static Badge](https://img.shields.io/badge/Template-Copier?style=for-the-badge&label=Copier&color=%23FFD000)
![Static Badge](https://img.shields.io/badge/MIT-License?style=for-the-badge&label=LICENSE&color=%2326ED46)

## Usage

Use one of the two approaches below to create a new project in `~/Downloads/<project-slug>`

### Using `copier`

1. Install `copier` and related Python libraries
   ```bash
   pip install copier jinja2-time copier-template-extensions
   ```
2. Create a new project from the `copier` template
   ```bash
   copier copy https://github.com/edesz/cpds-template.git ~/.Downloads
   ```
   where
   - `https://github.com/edesz/cpds-template.git`
     - is the [`src_path` in `copier copy`](https://copier.readthedocs.io/en/stable/reference/main/#copier._main.Worker) and it is the remote path to the `copier` template
   - `~/.Downloads`
     - is the [`dst_path` in `copier copy`](https://copier.readthedocs.io/en/stable/reference/main/#copier._main.Worker) and it is the destination path where to render the templated project

### Using `copier` with `pixi`

1. Install `pixi` using the [official `pixi` documentation](https://pixi.sh/latest/installation/).
2. Create a temporary directory at `~/Downloads/projects`.
3. Place the following `pixi.toml` file in the temporary directory
   ```bash
   # ~/Downloads/projects/pixi.toml
   [workspace]
   name = "cpds-template"
   channels = ["conda-forge"]
   platforms = ["linux-64"]
   version = "0.1.0"

   [dependencies]
   python = ">3.10"

   [pypi-dependencies]
   copier = "*"
   jinja2-time = "*"
   copier-template-extensions = "*"

   [tasks]
   start = "copier copy https://github.com/edesz/cpds-template.git ../Downloads --trust"
   ```
4. Configure `pixi.toml` for use
   - without downloading the `copier` template
     - no changes required
   - after downloading the template
     - clone the template locally to `~/Downloads` using
       ```bash
       git clone https://github.com/edesz/cpds-template.git
       ```
     - replace the last line of `pixi.toml` with the following
       ```bash
       start = "copier copy ../cpds-template . --trust"
       ```
       where
       - `../cpds-template` resolves to `~/Downloads/cpds-template`
         - this is the `copier copy` source template path (`src_path`), which is a string that can be resolved to the local path to the cloned `copier` template
       - `.` resolves to `~/Downloads`
         - this is the `copier copy` destination path (`dst_path`), which is the destination path where to render the templated project
5. Change into the temorary directory
   ```bash
   cd Downloads/projects
   ```
6. Create a new project from the `copier` template
   ```bash
   pixi run start
   ```
   which will create a new project in `~/Downloads/<project-slug>`.

## To Be Done

1. Write [tests for this `copier` template](https://github.com/noirbizarre/pytest-copier?tab=readme-ov-file#pytest-copier).
2. Add demo notebook.
3. Run demo notebook using `papermill_runner.py` with a [`copier` task](https://copier.readthedocs.io/en/stable/configuring/#tasks) (post-gen hook).
