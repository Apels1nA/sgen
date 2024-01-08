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


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ""
    with open(fname) as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError("Cannot find version information")
    return version


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content


setup(
    name="sgen",
    version=find_version("src/sgen/__init__.py"),
    description=(
        "Generating test data structures"
    ),
    long_description=read("README.rst"),
    author="Ilya Verner",
    url="https://github.com/Apels1nA/sgen/",
    packages=find_packages("src"),
    package_dir={"": "src"},
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
