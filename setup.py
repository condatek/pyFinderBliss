from setuptools import setup, find_packages

setup(
    name="pyFinderBliss",
    version="0.1.5ALPHA",
    description="A library to interact with FINDER BLISS thermostats",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Oliver Lee Chachou",
    author_email="olli90.ita@gmail.com",
    url="https://github.com/condatek/pyFinderBliss",
    packages=find_packages(),
    install_requires=[],  # Add any dependencies here
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
