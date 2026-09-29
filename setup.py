"""Packaging configuration for ASCII Generator."""

from pathlib import Path

from setuptools import find_packages, setup


ROOT_DIR = Path(__file__).parent
README_PATH = ROOT_DIR / "README.md"


setup(
    name="ascii-generator",
    version="1.0.0",
    description="Generate ASCII art from text, shapes, patterns, images, and natural-language commands.",
    long_description=README_PATH.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="JoaoTomas991",
    url="https://github.com/JoaoTomas991/ascii_generator",
    license="MIT",
    packages=find_packages(),
    py_modules=["run"],
    include_package_data=True,
    python_requires=">=3.12",
    extras_require={
        "images": ["Pillow>=10.0"],
    },
    entry_points={
        "console_scripts": [
            "ascii-generator=run:main",
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
