import codecs
import os
import re
import sys

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find version string.")

setup(
    name = "cloudburst",
    version = find_version("src", "cloudburst", "__init__.py"),
    description = "AWS Garbage collection tool",
    url = "https://www.brightband.io/products/cloudburst",
    keywords = "AWS garbage collection collector cloud cost manager management",
    package_dir={"": "src"},
    scripts = [
        "src/bin/cloudburst"
    ],
    packages=find_packages(
        where="src",
        exclude=["docs", "tests*", "bin"],
    ),
    zip_safe=False
)
