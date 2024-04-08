import re

from setuptools import setup, find_packages


EXTRAS_REQUIRE = {
    "tests": ["pytest"],
    "docs": [
        "sphinx==7.2.6",
        "sphinx-issues==3.0.1",
        "alabaster==0.7.13",
    ],
}


def find_version(file_name):
    """
    Attempts to find the version number in the file names file_name.
    Raises RuntimeError if not found.
    """

    pattern = re.compile(r'__version__ = \"\d+\.\d+\.\d+\"')

    with open(file_name) as file:
        lines = ' '.join(map(str.strip, file.readlines()))

    matches = re.findall(pattern, lines)

    if not matches:
        raise RuntimeError("Cannot find version information")

    return matches[0].split('"')[-2]


def read(file_name):
    with open(file_name) as fp:
        content = fp.read()
    return content


setup(
    name="sgen",
    version=find_version("sgen/__init__.py"),
    description="Generating test data structures",
    long_description=read("README.rst"),
    author="Ilya Verner",
    url="https://github.com/Apels1nA/sgen/",
    package_dir={"sgen": "sgen"},
    install_requires=["packaging>=17.0"],
    extras_require=EXTRAS_REQUIRE,
    license="MIT",
    zip_safe=False,
    keywords=[
        "generate",
        "data",
        "json",
        "test",
        "schema",
        "structure",
    ],
    python_requires=">=3.8",
    project_urls={
        "Repo": "https://github.com/Apels1nA/sgen",
        "Docs": "https://sgen.readthedocs.io/en/latest/index.html",
        "Changelog": "https://sgen.readthedocs.io/en/latest/changelog.html",
        "Issues": "https://github.com/Apels1nA/sgen/issues",
    },
)
