"""Packaging configuration for ASCII Art Generator."""

from pathlib import Path

from setuptools import find_packages, setup


ROOT_DIR = Path(__file__).parent
README_PATH = ROOT_DIR / "README.md"

# Optional dependencies, installed with e.g. pip install -e ".[all]". Keep the
# versions in step with requirements.txt.
EXTRAS = {
    "images": ["Pillow>=10.0"],  # convert image ...
    "fonts": ["pyfiglet>=1.0"],  # FIGlet fonts for write ...
}
EXTRAS["all"] = [dep for deps in EXTRAS.values() for dep in deps]


setup(
    name="ascii-art-generator",
    version="1.0.0",
    description="Generate ASCII art from text, shapes, patterns, images, and natural-language commands.",
    long_description=README_PATH.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="JoaoTomas991",
    url="https://github.com/JoaoTomas991/ascii-art-generator",
    license="MIT",
    packages=find_packages(),
    py_modules=["run"],
    include_package_data=True,
    python_requires=">=3.12",
    extras_require=EXTRAS,
    entry_points={
        "console_scripts": [
            "ascii-art-generator=run:main",
            "ascii-generator=run:main",  # short alias, kept from the first name
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Artistic Software",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Utilities",
    ],
    keywords="ascii art generator terminal cli",
)
