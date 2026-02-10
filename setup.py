from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="adzuna_api",
    version="0.1.0",
    author="Omar Moreno",
    description="A Python module to make it easier to use Adzuna API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moreno-omar/adzuna_api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "adzuna=adzuna_api.cli:main",
        ],
    },
)
