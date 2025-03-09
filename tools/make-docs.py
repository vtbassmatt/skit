import os.path
import pathlib
import pdoc
import tomllib


BASE_DIR = os.path.dirname(__file__)
ROOT_DIR = pathlib.Path(BASE_DIR, '..')
DOCS_DIR = pathlib.Path(ROOT_DIR, 'docs_out')


with open(ROOT_DIR / "pyproject.toml", 'rb') as toml_in:
    project_data = tomllib.load(toml_in)
version = project_data['project']['version']

pdoc.render.configure(
    footer_text = f'Skit {version}',
)
pdoc.pdoc('skit', output_directory=DOCS_DIR)
