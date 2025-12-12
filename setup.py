"""Setup script for Papagan - The Chatter Parrot."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="papagan-conversational-agent",
    version="1.0.0",
    author="Papagan",
    description="Azure AI-powered conversational agent - The Chatter Parrot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/orkinosai25-org/papagan-conversational-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "papagan-agent=main",
        ],
    },
    py_modules=["main"],
)
