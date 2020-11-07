import sys

from setuptools import find_packages, setup

requires = ["pytorch-pfn-extras"]

if sys.version_info.major == 3 and sys.version_info.minor < 7:
    requires.append("dataclasses")

extras = {
    "test": [
        "flake8",
        "autopep8",
        "black",
        "isort",
        "mypy",
        "pytest",
    ],
}

setup(
    name="python-config",
    version="0.0.0",
    install_requires=requires,
    test_requires=extras["test"],
    extras_require=extras,
    packages=find_packages(),
)
