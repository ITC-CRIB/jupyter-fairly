"""
jupyterfair setup
"""
import json
import sys
from pathlib import Path

import setuptools
import random

HERE = Path(__file__).parent.resolve()

# Get the package info from package.json
pkg_json = json.loads((HERE / "package.json").read_bytes())

# The name of the project
name = "jupyterfair"

lab_path = (HERE / pkg_json["jupyterlab"]["outputDir"])

# Representative files that should exist after a successful build
ensured_targets = [
    str(lab_path / "package.json"),
    str(lab_path / "static/style.js")
]

labext_name = pkg_json["name"]

data_files_spec = [
    ("share/jupyter/labextensions/%s" % labext_name, str(lab_path.relative_to(HERE)), "**"),
    ("share/jupyter/labextensions/%s" % labext_name, str("."), "install.json"),
    ("etc/jupyter/jupyter_server_config.d",
     "jupyter-config/server-config", "jupyterfair.json"),
    # For backward compatibility with notebook server
    ("etc/jupyter/jupyter_notebook_config.d",
     "jupyter-config/nb-config", "jupyterfair.json"),
]

long_description = (HERE / "README.md").read_text()

version = (
    pkg_json["version"]
    .replace("-alpha.", "a")
    .replace("-beta.", "b")
    .replace("-rc.", "rc")
) 

setup_args = dict(
    name=name,
    version=version,
    url=pkg_json["homepage"],
    author=pkg_json["author"]["name"],
    author_email=pkg_json["author"]["email"],
    description=pkg_json["description"],
    license=pkg_json["license"],
    license_file="LICENSE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=[
        "jupyter_server>=1.6,<2",
        "requests>=2.27.1",
        "python-dotenv==0.20.0",
        'pytest==7.1.2',
        "jupyter-packaging==0.12.0",
        "nodejs==0.1.1",
        "fairly==0.2.1"
    ],
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.7",
    platforms="Linux, Mac OS X, Windows",
    keywords=["Jupyter", "JupyterLab", "JupyterLab3"],
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Framework :: Jupyter",
        "Framework :: Jupyter :: JupyterLab",
        "Framework :: Jupyter :: JupyterLab :: 3",
        "Framework :: Jupyter :: JupyterLab :: Extensions",
        "Framework :: Jupyter :: JupyterLab :: Extensions :: Prebuilt",
    ],
)

# Create directory with dummy files in tests/fixtures/project_example
# This is to ensure that the project is testable
# Make directory in ./tests/fixtures/project_example
# DUMMY_PROJECT = "jupyterfair/tests/fixtures/dummy_project"
# (HERE / DUMMY_PROJECT).mkdir(parents=True, exist_ok=True)
# # Create dummy files in ./tests/fixtures/project_example

# def create_file(n, d, path, file_name):
#     '''
#     Makes a file in the given path containing data with random numbers
#     n: number of lines to make
#     d: number of characters to make each line
#     path: path to make file in
#     file_name: name of file to make

#     example create a 100 MB file
#     create_file(10**5, 100, <target_path>, <file_name>")
#     example create a 1 GB file
#     create_file(10**6, 100, <target_path>, <file_name>")
#     '''
#     f = open(f'{path}/{file_name}', 'w')
#     for i in range(n):
#         nums = [str(round(random.uniform(0, 1000 * 1000), 3)) for j in range(d)]
#         f.write(' '.join(nums))
#         f.write('\n')
#     f.close()

try:
    from jupyter_packaging import (
        wrap_installers,
        npm_builder,
        get_data_files
    )
    post_develop = npm_builder(
        build_cmd="install:extension", source_dir="src", build_dir=lab_path
    )
    setup_args["cmdclass"] = wrap_installers(post_develop=post_develop, ensured_targets=ensured_targets)
    setup_args["data_files"] = get_data_files(data_files_spec)
except ImportError as e:
    import logging
    logging.basicConfig(format="%(levelname)s: %(message)s")
    logging.warning("Build tool `jupyter-packaging` is missing. Install it with pip or conda.")
    if not ("--name" in sys.argv or "--version" in sys.argv):
        raise e

if __name__ == "__main__":
    # # if dummy project with dummy files doesnt exists, create it
    # if not (HERE / DUMMY_PROJECT).exists():
    #     # Create small file
    #     create_file(10, 100, HERE / DUMMY_PROJECT, "file_1MB.txt"))    
    
    #     # Create 10 files of 100 MB each
    #     for i in range(10):
    #         # check if file exists
    #         if not (HERE / DUMMY_PROJECT / f'file{i}.txt').exists():
    #             create_file(10**5, 100, DUMMY_PROJECT, f'file{i}.txt')
    
    setuptools.setup(**setup_args)
