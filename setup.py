from setuptools import setup, find_packages

setup(
    name="videomatic",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "torch",
        "diffusers",
        "Pillow",
        "pyyaml",
        "flask",
    ],
)